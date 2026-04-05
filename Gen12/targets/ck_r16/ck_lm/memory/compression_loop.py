"""
compression_loop.py — CK Memory: MAGMA dual-stream compression

Two streams (MAGMA, arXiv 2601.03236):
    FAST  — immediate write on every event, no generator inference, zero latency
    SLOW  — batch upgrade: full generator extraction, DBC27 routing, path extension

The fast stream ensures nothing is lost. The slow stream builds meaning.
This is how perception stays continuous while compression stays deep.

Loop frequency:
    Fast write:  every event (called directly by perception loop)
    Slow batch:  every 5 seconds (called by compression_loop.run_once())

© 2026 Brayden Sanders / 7Site LLC
"""

from __future__ import annotations
import uuid
import time
import threading
from typing import Optional, Callable

from .event_schema import Atom, PRIVATE, TEXT, INTERNAL
from .atom_store import write_atom, get_atom
from .dbc27 import build_key, key_from_atom

# Raw buffer: list of atom IDs pending slow upgrade
_raw_buffer: list[str] = []
_buffer_lock = threading.Lock()

# Slow stream interval (seconds)
SLOW_INTERVAL = 5.0

# Pluggable generator extractor — set by caller
# Signature: (raw_text: str) -> list[str]
_generator_extractor: Optional[Callable[[str], list[str]]] = None

# Pluggable lens encoder — set by caller
# Signature: (generators: list[str]) -> str  ("STRUCTURE" or "FLOW")
_lens_encoder: Optional[Callable[[list[str]], str]] = None


def set_generator_extractor(fn: Callable[[str], list[str]]) -> None:
    global _generator_extractor
    _generator_extractor = fn


def set_lens_encoder(fn: Callable[[list[str]], str]) -> None:
    global _lens_encoder
    _lens_encoder = fn


def fast_write(
    raw_text: str,
    modality: str = TEXT,
    privacy: str = PRIVATE,
    force_vector: Optional[list[float]] = None,
) -> str:
    """Immediate write — no generator inference, zero latency.

    Writes a raw atom with empty generators and dbc27_key='UNKNOWN'.
    Queues for slow upgrade.

    Returns atom_id.
    """
    atom = Atom(
        id=str(uuid.uuid4()),
        timestamp=time.time(),
        modality=modality,
        raw_ref=raw_text[:512] if raw_text else None,  # keep first 512 chars as ref
        generators=[],
        force_vector=force_vector or [0.5, 0.5, 0.5, 0.5, 0.5],
        operator=0,
        lens='FLOW',
        privacy=privacy,
        confidence=0.0,          # not yet scored
        compression_score=0.0,
    )
    write_atom(atom, dbc27_key='UNKNOWN')

    with _buffer_lock:
        _raw_buffer.append(atom.id)

    return atom.id


def slow_upgrade(atom_id: str) -> bool:
    """Upgrade a raw atom: extract generators, compute DBC27 key, update store.

    Returns True if upgrade succeeded.
    """
    atom = get_atom(atom_id)
    if not atom:
        return False
    if not atom.raw_ref:
        return False

    # Generator extraction
    generators: list[str] = []
    if _generator_extractor:
        try:
            generators = _generator_extractor(atom.raw_ref)
        except Exception:
            generators = []

    if not generators:
        # Fallback: use first 3 words as generators
        generators = atom.raw_ref.split()[:3]

    # Lens encoding
    lens = 'FLOW'
    if _lens_encoder:
        try:
            lens = _lens_encoder(generators)
        except Exception:
            lens = 'FLOW'

    # Update atom in store with full encoding
    secondary_op = (atom.operator + 1) % 10
    dbc27_key = build_key(atom.force_vector, atom.operator, secondary_op, lens)

    atom.generators = generators
    atom.lens = lens
    atom.confidence = 0.5          # now scorable
    atom.compression_score = min(1.0, len(generators) / max(1, len(atom.raw_ref.split())))

    write_atom(atom, dbc27_key=dbc27_key)
    return True


def run_once() -> dict:
    """Process the slow upgrade queue. Call every SLOW_INTERVAL seconds.

    Returns stats dict.
    """
    with _buffer_lock:
        batch = list(_raw_buffer)
        _raw_buffer.clear()

    upgraded = 0
    failed = 0
    for atom_id in batch:
        if slow_upgrade(atom_id):
            upgraded += 1
        else:
            failed += 1

    return {
        'batch_size': len(batch),
        'upgraded': upgraded,
        'failed': failed,
        'timestamp': time.time(),
    }


class CompressionLoop:
    """Background thread that runs the slow upgrade loop at SLOW_INTERVAL."""

    def __init__(self, interval: float = SLOW_INTERVAL):
        self.interval = interval
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self.stats: list[dict] = []

    def start(self) -> None:
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()

    def _run(self) -> None:
        while not self._stop.wait(self.interval):
            result = run_once()
            if result['batch_size'] > 0:
                self.stats.append(result)
                if len(self.stats) > 1000:
                    self.stats = self.stats[-500:]
