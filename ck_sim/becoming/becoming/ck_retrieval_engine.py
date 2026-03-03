"""
ck_retrieval_engine.py -- D2 Knowledge Retrieval (No Vectors, No LLM)
=====================================================================
Operator: COUNTER (2) -- measuring curvature to find knowledge.

CK's retrieval layer uses its own math (D2 curvature) instead of
vector embeddings. Every text chunk is converted to a 10-value
operator distribution. Queries are matched via KL divergence on
those distributions plus D2 curvature similarity.

Architecture:
  1. CHUNK STORE - text split into ~500-char chunks, each with
     its operator signature (10-value distribution).
  2. D2 MATCHING - query → operator distribution → compare to
     all stored chunks → return top matches.
  3. RETRIEVAL LOOP - query → D2 → match → extract → recompose.

The "Outside Library" is a folder of text files. CK reads them,
computes their operator signatures, and stores only the signatures
plus chunk references. Retrieval is pure math.

This gives CK PhD-level recall without ANY LLM.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import json
import os
import math
from collections import Counter
from typing import Dict, List, Tuple, Optional

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, OP_NAMES, CL, compose
)
from ck_sim.ck_sim_d2 import D2Pipeline, soft_classify_d2


# ================================================================
#  TEXT → OPERATOR DISTRIBUTION
# ================================================================

def text_to_operator_dist(text: str) -> List[float]:
    """Convert text to a 10-value operator distribution via D2.

    Each letter triplet → D2 curvature → operator.
    Returns normalized histogram (sums to 1.0).
    """
    pipe = D2Pipeline()
    counts = [0] * NUM_OPS

    for ch in text.lower():
        if 'a' <= ch <= 'z':
            idx = ord(ch) - ord('a')
            if pipe.feed_symbol(idx):
                counts[pipe.operator] += 1

    total = sum(counts)
    if total == 0:
        return [0.0] * NUM_OPS
    return [c / total for c in counts]


def text_to_mean_d2(text: str) -> List[float]:
    """Compute mean 5D D2 vector for text.

    Used for finer-grained matching when operator distributions
    are similar. The 5D vector captures the curvature shape,
    not just which operator dominates.
    """
    pipe = D2Pipeline()
    d2_sum = [0.0] * 5
    n = 0

    for ch in text.lower():
        if 'a' <= ch <= 'z':
            idx = ord(ch) - ord('a')
            if pipe.feed_symbol(idx):
                for i in range(5):
                    d2_sum[i] += pipe.d2_float[i]
                n += 1

    if n == 0:
        return [0.0] * 5
    return [s / n for s in d2_sum]


# ================================================================
#  SIMILARITY METRICS
# ================================================================

def kl_divergence(p: List[float], q: List[float],
                  epsilon: float = 1e-10) -> float:
    """KL divergence D_KL(P || Q).

    Measures how different distribution P is from Q.
    Lower = more similar. 0 = identical.
    Uses epsilon smoothing to avoid log(0).
    """
    total = 0.0
    for pi, qi in zip(p, q):
        pi = max(pi, epsilon)
        qi = max(qi, epsilon)
        total += pi * math.log(pi / qi)
    return total


def symmetric_kl(p: List[float], q: List[float]) -> float:
    """Symmetric KL divergence: (D_KL(P||Q) + D_KL(Q||P)) / 2.

    More stable than one-directional KL. Lower = more similar.
    """
    return (kl_divergence(p, q) + kl_divergence(q, p)) / 2.0


def d2_cosine_similarity(a: List[float], b: List[float]) -> float:
    """Cosine similarity between two 5D D2 vectors.

    Returns value in [-1, 1]. Higher = more similar.
    """
    dot = sum(ai * bi for ai, bi in zip(a, b))
    mag_a = math.sqrt(sum(ai * ai for ai in a))
    mag_b = math.sqrt(sum(bi * bi for bi in b))
    if mag_a < 1e-10 or mag_b < 1e-10:
        return 0.0
    return dot / (mag_a * mag_b)


def combined_similarity(query_dist: List[float], query_d2: List[float],
                        chunk_dist: List[float], chunk_d2: List[float],
                        w_kl: float = 0.6, w_cos: float = 0.4) -> float:
    """Combined similarity score using KL divergence + D2 cosine.

    Returns a score where HIGHER = more similar.
    KL divergence is inverted (1 / (1 + kl)) so higher = better.

    Args:
        w_kl: weight for operator distribution match (default 0.6)
        w_cos: weight for D2 curvature shape match (default 0.4)
    """
    kl = symmetric_kl(query_dist, chunk_dist)
    cos = d2_cosine_similarity(query_d2, chunk_d2)

    # Convert KL to similarity (higher = better)
    kl_sim = 1.0 / (1.0 + kl)

    # Cosine is already in [-1, 1], map to [0, 1]
    cos_sim = (cos + 1.0) / 2.0

    return w_kl * kl_sim + w_cos * cos_sim


# ================================================================
#  CHUNK STORE
# ================================================================

class TextChunk:
    """A chunk of text with its D2 operator signature."""

    __slots__ = ['text', 'source', 'chunk_id', 'op_dist', 'mean_d2',
                 'dominant_op', 'cl_fuse']

    def __init__(self, text: str, source: str = '', chunk_id: int = 0):
        self.text = text
        self.source = source
        self.chunk_id = chunk_id

        # Compute operator signature
        self.op_dist = text_to_operator_dist(text)
        self.mean_d2 = text_to_mean_d2(text)

        # Derived
        self.dominant_op = max(range(NUM_OPS), key=lambda i: self.op_dist[i])

        # CL fuse of operator chain
        pipe = D2Pipeline()
        ops = []
        for ch in text.lower():
            if 'a' <= ch <= 'z':
                if pipe.feed_symbol(ord(ch) - ord('a')):
                    ops.append(pipe.operator)
        if ops:
            fused = ops[0]
            for op in ops[1:]:
                fused = compose(fused, op)
            self.cl_fuse = fused
        else:
            self.cl_fuse = VOID

    def to_dict(self) -> dict:
        """Serialize for JSON storage (text stored separately)."""
        return {
            'source': self.source,
            'chunk_id': self.chunk_id,
            'op_dist': [round(d, 4) for d in self.op_dist],
            'mean_d2': [round(d, 6) for d in self.mean_d2],
            'dominant_op': self.dominant_op,
            'cl_fuse': self.cl_fuse,
        }


class ChunkStore:
    """Storage and retrieval for text chunks.

    Stores chunks with their D2 operator signatures.
    Retrieval uses combined KL divergence + D2 cosine similarity.
    """

    def __init__(self):
        self.chunks: List[TextChunk] = []
        self._next_id = 0

    def add_text(self, text: str, source: str = '',
                 chunk_size: int = 500, overlap: int = 50) -> int:
        """Add text, splitting into chunks.

        Args:
            text: full text to chunk and index
            source: origin identifier (filename, URL, etc.)
            chunk_size: target characters per chunk
            overlap: character overlap between chunks

        Returns:
            Number of chunks created.
        """
        chunks_added = 0
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))

            # Try to break at sentence boundary
            if end < len(text):
                for sep in ['. ', '.\n', '! ', '? ', '\n\n']:
                    last_sep = text[start:end].rfind(sep)
                    if last_sep > chunk_size // 2:
                        end = start + last_sep + len(sep)
                        break

            chunk_text = text[start:end].strip()
            if len(chunk_text) > 20:  # Skip tiny fragments
                chunk = TextChunk(chunk_text, source, self._next_id)
                self.chunks.append(chunk)
                self._next_id += 1
                chunks_added += 1

            start = end - overlap if end < len(text) else len(text)

        return chunks_added

    def add_file(self, path: str) -> int:
        """Add a text file to the store."""
        if not os.path.exists(path):
            return 0
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        source = os.path.basename(path)
        return self.add_text(text, source=source)

    def add_directory(self, directory: str, extensions: tuple = ('.txt', '.md')) -> int:
        """Add all text files from a directory."""
        total = 0
        if not os.path.isdir(directory):
            return 0
        for root, dirs, files in os.walk(directory):
            for fname in files:
                if fname.lower().endswith(extensions):
                    path = os.path.join(root, fname)
                    total += self.add_file(path)
        return total

    def query(self, query_text: str, top_k: int = 5,
              min_similarity: float = 0.3) -> List[Tuple[TextChunk, float]]:
        """Find the most relevant chunks for a query.

        Args:
            query_text: the question or topic to search for
            top_k: number of results to return
            min_similarity: minimum similarity threshold

        Returns:
            List of (chunk, similarity_score) tuples, best first.
        """
        if not self.chunks:
            return []

        query_dist = text_to_operator_dist(query_text)
        query_d2 = text_to_mean_d2(query_text)

        scored = []
        for chunk in self.chunks:
            sim = combined_similarity(
                query_dist, query_d2,
                chunk.op_dist, chunk.mean_d2
            )
            if sim >= min_similarity:
                scored.append((chunk, sim))

        scored.sort(key=lambda x: -x[1])
        return scored[:top_k]

    def query_by_operator(self, target_op: int, top_k: int = 5) -> List[Tuple[TextChunk, float]]:
        """Find chunks dominated by a specific operator.

        Useful for: "find me everything about growth" → PROGRESS
        """
        results = []
        for chunk in self.chunks:
            strength = chunk.op_dist[target_op]
            if strength > 0.1:
                results.append((chunk, strength))
        results.sort(key=lambda x: -x[1])
        return results[:top_k]

    def stats(self) -> dict:
        """Store statistics."""
        if not self.chunks:
            return {'total_chunks': 0}

        op_counts = Counter(c.dominant_op for c in self.chunks)
        sources = Counter(c.source for c in self.chunks)

        return {
            'total_chunks': len(self.chunks),
            'by_dominant_op': {OP_NAMES[i]: op_counts.get(i, 0) for i in range(NUM_OPS)},
            'by_source': dict(sources),
            'avg_chunk_len': sum(len(c.text) for c in self.chunks) / len(self.chunks),
        }

    def save_signatures(self, path: str):
        """Save chunk signatures (without text) to JSON.

        Stores only operator distributions and metadata.
        Text chunks stored separately for space efficiency.
        """
        data = {
            'n_chunks': len(self.chunks),
            'chunks': [c.to_dict() for c in self.chunks],
            'texts': [c.text for c in self.chunks],
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=1)

    def load_signatures(self, path: str):
        """Load chunk signatures from JSON."""
        if not os.path.exists(path):
            return
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.chunks = []
        texts = data.get('texts', [])
        for i, cdata in enumerate(data.get('chunks', [])):
            text = texts[i] if i < len(texts) else ''
            chunk = TextChunk(text, cdata.get('source', ''), cdata.get('chunk_id', i))
            # Override computed values with stored ones
            chunk.op_dist = cdata.get('op_dist', chunk.op_dist)
            chunk.mean_d2 = cdata.get('mean_d2', chunk.mean_d2)
            chunk.dominant_op = cdata.get('dominant_op', chunk.dominant_op)
            chunk.cl_fuse = cdata.get('cl_fuse', chunk.cl_fuse)
            self.chunks.append(chunk)
        self._next_id = len(self.chunks)


# ================================================================
#  RETRIEVAL ENGINE (Full Pipeline)
# ================================================================

class RetrievalEngine:
    """CK's knowledge retrieval system.

    Pipeline:
      query → D2 signature → match chunks → extract text → return

    Usage:
        engine = RetrievalEngine()
        engine.ingest_directory('path/to/library/')
        results = engine.retrieve("what is photosynthesis?")
        for text, score in results:
            print(f"[{score:.2f}] {text[:100]}...")
    """

    def __init__(self):
        self.store = ChunkStore()

    def ingest_text(self, text: str, source: str = '') -> int:
        """Add text to the knowledge base."""
        return self.store.add_text(text, source)

    def ingest_file(self, path: str) -> int:
        """Add a file to the knowledge base."""
        return self.store.add_file(path)

    def ingest_directory(self, directory: str) -> int:
        """Add all text files from a directory."""
        return self.store.add_directory(directory)

    def ingest_library(self, library_path: str) -> int:
        """Ingest CK's library (ck_library/ folder with domain subfolders).

        Each subfolder has chains.json and meta.json.
        Also ingests any .txt or .md files found.
        """
        total = 0

        if not os.path.isdir(library_path):
            return 0

        # Walk through library domains
        for domain_dir in sorted(os.listdir(library_path)):
            domain_path = os.path.join(library_path, domain_dir)
            if not os.path.isdir(domain_path):
                continue

            # Ingest JSON metadata as text
            meta_path = os.path.join(domain_path, 'meta.json')
            if os.path.exists(meta_path):
                try:
                    with open(meta_path, 'r', encoding='utf-8') as f:
                        meta = json.load(f)
                    # Convert meta to text for chunking
                    meta_text = json.dumps(meta, indent=2)
                    total += self.store.add_text(
                        meta_text, source=f'library/{domain_dir}/meta')
                except (json.JSONDecodeError, IOError):
                    pass

            # Ingest any text files
            for fname in os.listdir(domain_path):
                if fname.endswith(('.txt', '.md')):
                    fpath = os.path.join(domain_path, fname)
                    total += self.store.add_file(fpath)

        return total

    def retrieve(self, query: str, top_k: int = 5,
                 min_similarity: float = 0.3) -> List[Tuple[str, float]]:
        """Retrieve relevant text for a query.

        Returns list of (text, score) tuples.
        """
        results = self.store.query(query, top_k, min_similarity)
        return [(chunk.text, score) for chunk, score in results]

    def retrieve_by_topic(self, target_op: int,
                          top_k: int = 5) -> List[Tuple[str, float]]:
        """Retrieve chunks by dominant operator.

        Example: retrieve_by_topic(PROGRESS) → everything about growth.
        """
        results = self.store.query_by_operator(target_op, top_k)
        return [(chunk.text, score) for chunk, score in results]

    def answer(self, query: str, top_k: int = 3) -> str:
        """Simple answer pipeline: retrieve + concatenate best chunks.

        For full answer generation, use CKTalkLoop.explain()
        with the retrieved text.
        """
        results = self.retrieve(query, top_k)
        if not results:
            return "I do not have information about that."

        # Return best matching chunk
        return results[0][0]

    def save(self, path: str):
        """Save the knowledge base."""
        self.store.save_signatures(path)

    def load(self, path: str):
        """Load a knowledge base."""
        self.store.load_signatures(path)

    def stats(self) -> dict:
        """Knowledge base statistics."""
        return self.store.stats()


# ================================================================
#  CLI
# ================================================================

if __name__ == '__main__':
    import sys

    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    print("=" * 60)
    print("  CK RETRIEVAL ENGINE")
    print("=" * 60)

    engine = RetrievalEngine()

    # Try to ingest library
    lib_paths = [
        os.path.join(base, 'CKIS', 'ck_library'),
        os.path.join(base, 'ck_library'),
    ]
    for lib_path in lib_paths:
        if os.path.isdir(lib_path):
            n = engine.ingest_library(lib_path)
            print(f"\n  Ingested {n} chunks from {lib_path}")

    # Try to ingest knowledge docs
    knowledge_paths = [
        os.path.join(base, 'CKIS', 'knowledge'),
        os.path.join(base, 'knowledge'),
    ]
    for kp in knowledge_paths:
        if os.path.isdir(kp):
            n = engine.ingest_directory(kp)
            print(f"  Ingested {n} chunks from {kp}")

    stats = engine.stats()
    print(f"\n  Total chunks: {stats['total_chunks']}")
    if 'by_dominant_op' in stats:
        print(f"\n  By dominant operator:")
        for op_name, count in stats['by_dominant_op'].items():
            if count > 0:
                print(f"    {op_name:12s}: {count}")

    # Interactive query mode
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
    else:
        query = "What is coherence?"

    print(f"\n  Query: \"{query}\"")
    results = engine.retrieve(query, top_k=3)
    for i, (text, score) in enumerate(results):
        preview = text[:120].replace('\n', ' ')
        print(f"\n  [{i+1}] Score: {score:.3f}")
        print(f"      {preview}...")
