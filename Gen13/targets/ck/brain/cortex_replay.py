# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0 (DOI: 10.5281/zenodo.18852047)
"""
cortex_replay.py -- feed his history through the cortex so the Hebbian
field actually LEARNS from it, instead of the engine merely reciting it.

Why this exists:
  CK currently has two voice-paths for recalled facts.  Both are templates:

    ck_truth_recall   -- literal string retrieval from ck_truth.py
    ck_fractal_dual   -- dictionary tokens stitched onto operator arcs

  Neither is "him speaking from what he learned" -- they're retrievals.

  The cortex (ao_5element + hebbian_5x5_cl + quadratic_glue) is the piece
  that DOES learn.  Every symbol fed through cortex.step_text() updates
  the 5x5 W matrix and grows the emergent signal.  But until now the
  cortex only saw LIVE CHAT TEXT -- a few hundred symbols per session.

  This module feeds him HIS HISTORY -- sprint paper abstracts, the brain
  design docs, the 2->3 bridge paper -- through the same cortex pathway.
  After replay, his Hebbian field reflects the topics Brayden has been
  working on, and the live voice readouts actually have something to say
  about flatness, crossing lemma, xi cosmology, sigma rate, quadratic glue.

  The replay does NOT populate ck_truth_recall (that would be more
  templates).  It feeds the TEXT as symbols, so the learning is genuine.

Design:
  - `DEFAULT_SOURCES` names the high-value Gen12/Gen13 files to replay.
  - `replay_file(cortex, path, max_bytes)` reads and feeds one file.
  - `replay_many(cortex, paths)` batches, reports per-source ticks.
  - `main()` boots a cortex from persisted state, replays DEFAULT_SOURCES,
    saves, prints before/after stats.
  - Idempotent-ish: replaying the same text twice still adds to W (Hebbian
    is naturally rate-limited by decay), but you generally want to replay
    once to seed, then let live chat extend it.

Usage:
    python Gen13/targets/ck/brain/cortex_replay.py
"""

from __future__ import annotations

import os
import sys
import time
from typing import Iterable, List, Optional, Tuple

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

# Walk up to the repo root so the DEFAULT_SOURCES can use repo-relative paths.
_REPO_ROOT = os.path.abspath(os.path.join(_HERE, "..", "..", "..", ".."))


# ── Default source set ────────────────────────────────────────────────
# Curated to cover the frontier topics where fractal-voice currently
# falls through with no structural grounding: flatness theorem, crossing
# lemma, xi cosmology, sigma rate, 2->3 bridge.  Also includes the Gen13
# brain design docs so he learns HIS OWN architecture, not just external
# frontier work.
DEFAULT_SOURCES: List[str] = [
    # Gen13 -- his own architecture (highest priority)
    "Gen13/targets/ck/brain/BRAIN_DESIGN.md",
    "Gen13/targets/ck/brain/NEURAL_INVENTORY.md",
    "Gen13/README_GEN13.md",
    "Gen13/ARCHITECTURE.md",
    # Sprint 10 -- flatness theorem + crossing lemma
    "Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/CROSSING_LEMMA.md",
    "Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/WP51_FLATNESS_THEOREM.md",
    "Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/WP52_D2_AS_RING_CURVATURE.md",
    "Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/WP57_CROSSING_LEMMA_ARC.md",
    # Sprint 14 -- xi cosmology + sigma rate theorem
    "Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/WP81_CANONICAL_XI_THEORY.md",
    "Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/WP82_LOG_QUINTESSENCE_NOVELTY.md",
    "Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/WP101_SIGMA_RATE_THEOREM.md",
    "Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/WP100_SPRINT_SYNTHESIS.md",
    # Sprint 35b -- Beauville / Hodge C_* explicit target (added 2026-04-18)
    # Two ClaudeChat foundation-side notes arrived on the desktop describing
    # what the Sprint 35b target invariants really are and a 12-point filter
    # for candidate curves. Dense AG / number-theory prose -> perfect Hebbian fuel.
    "Gen12/targets/clay/papers/sprint35b_beauville_explicit_2026_04_18/HODGE_CSTAR_TARGET_NOTE.md",
    "Gen12/targets/clay/papers/sprint35b_beauville_explicit_2026_04_18/WHAT_COUNTS_AS_A_GOOD_CSTAR.md",
    "Gen12/targets/clay/papers/sprint35b_beauville_explicit_2026_04_18/S35B_BEAUVILLE_EXPLICIT_PLAN.md",
    "Gen12/targets/clay/papers/sprint35b_beauville_explicit_2026_04_18/S35B_PATH_A_PROTOTYPE_STATUS.md",
    "Gen12/targets/clay/papers/sprint35b_beauville_explicit_2026_04_18/S35B_FRONTIER_UPDATE_2026_04_18.md",
    # The 2->3 bridge paper (lives in papers/, not clay/papers/)
    "papers/test_a15_quadratic_glue.py",
]

# Hard cap per file -- keeps replay time bounded even if someone points
# us at a 4 MB bible.  80 KB roughly matches a long whitepaper.
DEFAULT_MAX_BYTES_PER_FILE = 80_000


# ── Helpers ───────────────────────────────────────────────────────────

def _resolve(path: str) -> str:
    """If the given path is repo-relative, anchor it on _REPO_ROOT."""
    if os.path.isabs(path):
        return path
    return os.path.normpath(os.path.join(_REPO_ROOT, path))


def _read_text(path: str, max_bytes: int) -> str:
    """Read up to max_bytes of UTF-8 text.  Returns empty string if missing."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read(max_bytes)
    except (FileNotFoundError, OSError):
        return ""


def _count_letters(text: str) -> int:
    """Count a..z|A..Z letters -- matches what cortex.step_text will feed."""
    return sum(1 for ch in text if ("a" <= ch.lower() <= "z"))


# ── Replay a single file ──────────────────────────────────────────────

def replay_file(
    cortex,
    path: str,
    max_bytes: int = DEFAULT_MAX_BYTES_PER_FILE,
) -> Tuple[int, int, str]:
    """Feed one file through cortex.step_text().

    Args:
        cortex: a booted Cortex (will be mutated -- W grows, tick advances).
        path:   repo-relative or absolute path to a text/code file.
        max_bytes: cap on bytes read from the file.

    Returns:
        (ticks_added, bytes_read, resolved_path)
    """
    abspath = _resolve(path)
    text = _read_text(abspath, max_bytes)
    if not text:
        return (0, 0, abspath)
    tick_before = cortex.state.tick
    cortex.step_text(text)
    ticks_added = cortex.state.tick - tick_before
    return (ticks_added, len(text), abspath)


# ── Replay a batch ────────────────────────────────────────────────────

def replay_many(
    cortex,
    paths: Iterable[str] = None,
    max_bytes_per_file: int = DEFAULT_MAX_BYTES_PER_FILE,
    progress: bool = True,
) -> List[Tuple[str, int, int]]:
    """Feed a batch of files through the cortex.

    Returns a list of (path, ticks_added, bytes_read) per source."""
    if paths is None:
        paths = DEFAULT_SOURCES
    results: List[Tuple[str, int, int]] = []
    for p in paths:
        ticks, nbytes, abspath = replay_file(
            cortex, p, max_bytes=max_bytes_per_file
        )
        results.append((abspath, ticks, nbytes))
        if progress:
            short = os.path.relpath(abspath, _REPO_ROOT) if nbytes else p
            if nbytes:
                print(f"  [{ticks:6d} ticks] {short}  ({nbytes:,} bytes)")
            else:
                print(f"  [ MISSING ] {short}")
    return results


# ── __main__: boot cortex, load persisted state, replay, save ────────

def main(paths: Optional[List[str]] = None) -> int:
    """Replay his history into the live cortex state file."""
    from cortex import Cortex
    from cortex_persist import (
        load_cortex, save_cortex, DEFAULT_STATE_PATH,
    )

    paths = paths if paths is not None else DEFAULT_SOURCES
    cx = Cortex().boot()
    try:
        loaded = load_cortex(cx, DEFAULT_STATE_PATH)
    except Exception as e:
        print(f"[replay] load failed ({e}); starting cold")
        loaded = False
    if loaded:
        print(f"[replay] loaded prior state: tick={cx.state.tick} "
              f"W_trace={cx.state.W_trace:.4f}")
    else:
        print(f"[replay] no prior state; starting cold")

    print(f"[replay] feeding {len(paths)} sources through cortex "
          f"(max {DEFAULT_MAX_BYTES_PER_FILE:,} bytes each)")
    t0 = time.time()
    results = replay_many(cx, paths)
    elapsed = time.time() - t0

    total_ticks = sum(t for _, t, _ in results)
    total_bytes = sum(b for _, _, b in results)
    missing = sum(1 for _, _, b in results if b == 0)

    print(f"[replay] total: {total_ticks:,} ticks from {total_bytes:,} bytes "
          f"in {elapsed:.1f}s "
          f"({missing} missing)")
    print(f"[replay] post-state: tick={cx.state.tick} "
          f"emergent={cx.state.emergent:.4f} W_trace={cx.state.W_trace:.4f} "
          f"harmony_rate={cx.hebbian.harmony_rate():.4f}")
    print(f"[replay] strongest pair: {cx.state.W_strongest}")

    # Save back to disk so the live server picks it up on next restart
    # (or reload via /cortex/reload endpoint if we add one later).
    path = save_cortex(cx, DEFAULT_STATE_PATH)
    print(f"[replay] saved to: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
