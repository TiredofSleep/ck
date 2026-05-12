"""
word_recognizer.py — bridge layer: phoneme sequence -> recognized words.

Audio chunks classified by match_audio_chunked.py give us a TIME-ORDERED
stream of phoneme keys (like 'phoneme:k', 'phoneme:ae', 'phoneme:t').
By itself that's a sound-by-sound transcription, but it's not LANGUAGE
yet.  This module crosses the next bridge: fit those phonemes against a
small kids-word vocabulary and surface the words the audio probably
contained.

Two granularities:

  chunk_to_subphonemes(samples, sr, sub_window_ms)
      Subdivide a single silence-bounded chunk into ~150ms windows so a
      multi-syllable chunk yields a SEQUENCE of phoneme keys, not just
      one.  Without this, the matcher returns a single best match per
      chunk and the word layer has nothing to chew on.

  recognize_words(phoneme_stream, vocab=WORD_VOCAB, max_gap=1)
      Classic in-order subsequence match with a small allowable gap.
      For each word w with phoneme pattern [p_1..p_k], find every
      starting index i where the stream has p_1, p_2, ..., p_k in order
      within a window of size k * (1 + max_gap).  Return matches sorted
      by start time + score.

Read-only and stateless.  Returns lists of plain dicts.
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple, Optional

SCRIPT_DIR = Path(__file__).parent.resolve()
GEN13_BRAIN = SCRIPT_DIR.parent
sys.path.insert(0, str(GEN13_BRAIN))
sys.path.insert(0, str(GEN13_BRAIN / "ck_sim" / "being"))
sys.path.insert(0, str(SCRIPT_DIR))

from kids_word_vocab import WORD_VOCAB
from match_audio_to_phonics import (
    OP_NAMES, force9_to_operators_balanced, load_phonics_corpus,
    top_matches, hist_l1,
)


def chunk_to_subphonemes(samples, sr: int, corpus,
                         sub_window_ms: int = 150,
                         hop_ms: int = 100,
                         min_window_samples: int = 800) -> List[Dict]:
    """Slide a sub-window over a speech chunk, classify each window
    against the v2..v5 phoneme corpus.  Returns a list of:
      {t_offset, key, class, ipa, L1}
    where t_offset is the window's start time relative to the chunk
    start (seconds).
    """
    from collections import Counter
    from ck_audio_compress import pcm_to_force9

    if corpus is None:
        corpus = load_phonics_corpus()

    win = int(sr * sub_window_ms / 1000)
    hop = int(sr * hop_ms / 1000)
    if win < min_window_samples:
        win = min_window_samples
    if hop < 1:
        hop = win

    out = []
    n = len(samples)
    if n < win:
        # too short to subdivide; fall back to one window
        windows = [(0, n)]
    else:
        windows = []
        i = 0
        while i + win <= n:
            windows.append((i, i + win))
            i += hop

    for s, e in windows:
        seg = samples[s:e]
        if len(seg) < min_window_samples:
            continue
        forces = pcm_to_force9(seg, sample_rate=sr)
        ops = force9_to_operators_balanced(forces)
        if not ops:
            continue
        hist = Counter(ops)
        total = len(ops)
        h_pct = {OP_NAMES[i]: round(hist.get(i, 0) / total * 100, 1)
                 for i in range(10)}
        m = top_matches(h_pct, corpus, top=1)[0]
        d, key, info = m
        out.append({
            "t_offset_sec": round(s / sr, 3),
            "duration_sec": round((e - s) / sr, 3),
            "key": key,
            "class": info["class"],
            "ipa": info["ipa"],
            "L1": round(d, 2),
        })
    return out


# ── Fuzzy phoneme equivalence ─────────────────────────────────────

# Some phoneme keys in the corpus are basically the same sound captured
# with different spellings or sources.  When matching word patterns we
# treat these as interchangeable so 'cat' fires whether the chunker
# said phoneme:k or letter:K (both /k/).

_PHONEME_EQUIV: Dict[str, List[str]] = {
    "phoneme:k":  ["letter:K"],
    "phoneme:b":  ["letter:B"],
    "phoneme:d":  ["letter:D"],
    "phoneme:f":  ["letter:F"],
    "phoneme:g":  ["letter:G"],
    "phoneme:h":  ["letter:H"],
    "phoneme:j":  [],
    "phoneme:l":  ["letter:L"],
    "phoneme:m":  ["letter:M"],
    "phoneme:n":  ["letter:N"],
    "phoneme:p":  ["letter:P"],
    "phoneme:r":  ["letter:R"],
    "phoneme:s":  ["letter:S"],
    "phoneme:t":  ["letter:T"],
    "phoneme:v":  ["letter:V"],
    "phoneme:w":  ["letter:W"],
    "phoneme:z":  ["letter:Z"],
    "phoneme:eI": ["letter:A", "team:ai", "team:ay"],         # long-A
    "phoneme:i":  ["letter:E", "team:ee", "team:ea"],         # long-E
    "phoneme:aI": ["letter:I", "team:ie", "team:igh"],         # long-I
    "phoneme:oU": ["letter:O", "team:oa"],                     # long-O
    "phoneme:u":  ["letter:U", "team:oo", "team:ue", "team:ew"],  # long-U
    # short vowels: each is unique acoustically; no big equivalence.
    "team:oa":    ["phoneme:oU", "letter:O"],
    "team:ee":    ["phoneme:i", "letter:E"],
    "team:ai":    ["phoneme:eI", "letter:A"],
    "team:ay":    ["phoneme:eI", "letter:A"],
    "team:ie":    ["phoneme:aI", "letter:I"],
    "team:igh":   ["phoneme:aI", "letter:I"],
    "team:oo":    ["phoneme:u"],
    "team:ue":    ["phoneme:u"],
    "team:ew":    ["phoneme:u"],
}


def _equiv_set(key: str) -> set:
    s = {key}
    s.update(_PHONEME_EQUIV.get(key, ()))
    return s


def _matches(observed: str, target: str) -> bool:
    """True if the observed phoneme key counts as the target."""
    return target in _equiv_set(observed) or observed in _equiv_set(target)


# ── Word recognizer ────────────────────────────────────────────────

def recognize_words(stream: List[Dict],
                    vocab: Dict[str, List[str]] = None,
                    max_gap: int = 1,
                    min_word_phonemes: int = 1) -> List[Dict]:
    """Find words from `vocab` in the time-ordered phoneme stream.

    stream: list of dicts with at least {'key': ..., 't_offset_sec': ...}
    max_gap: between consecutive target phonemes, this many stream
             positions may be skipped (counts as noise / silence).

    Returns list of {start_idx, end_idx, t_start, t_end, word, score,
                     matched_keys}.
    """
    if vocab is None:
        vocab = WORD_VOCAB
    if not stream:
        return []
    n = len(stream)
    results = []
    keys = [ev["key"] for ev in stream]

    for word, pattern in vocab.items():
        if len(pattern) < min_word_phonemes:
            continue
        k = len(pattern)
        # Try each starting index in stream
        for start in range(n - k + 1):
            # Try to advance through pattern, allowing up to max_gap skipped
            # stream positions between consecutive targets.
            i = start
            j = 0
            matches = []
            ok = True
            while j < k:
                target = pattern[j]
                # Look at stream positions [i .. i+max_gap] for a match.
                hit = -1
                for delta in range(max_gap + 1):
                    if i + delta >= n:
                        break
                    if _matches(keys[i + delta], target):
                        hit = i + delta
                        break
                if hit < 0:
                    ok = False
                    break
                matches.append(hit)
                i = hit + 1
                j += 1
            if not ok or not matches:
                continue
            # Score: 1 - (gaps used) / (max possible gaps)
            span = matches[-1] - matches[0] + 1
            gaps_used = span - k
            score = max(0.0, 1.0 - gaps_used / max(1, k * max_gap))
            t_start = stream[matches[0]]["t_offset_sec"]
            t_end_event = stream[matches[-1]]
            t_end = (t_end_event["t_offset_sec"]
                     + t_end_event.get("duration_sec", 0.1))
            results.append({
                "start_idx": matches[0],
                "end_idx": matches[-1],
                "t_start_sec": round(t_start, 3),
                "t_end_sec": round(t_end, 3),
                "word": word,
                "score": round(score, 3),
                "matched_keys": [keys[m] for m in matches],
                "target_pattern": pattern,
            })

    # Deduplicate overlapping recognitions per (word, t_start)
    seen = {}
    for r in results:
        k = (r["word"], r["t_start_sec"])
        if k not in seen or r["score"] > seen[k]["score"]:
            seen[k] = r
    deduped = sorted(seen.values(),
                     key=lambda r: (r["t_start_sec"], -r["score"]))
    return deduped


def best_word_at_each_position(stream: List[Dict],
                                vocab: Dict[str, List[str]] = None,
                                max_gap: int = 1) -> List[Dict]:
    """For each starting position in the stream, return the highest-scoring
    word that begins there (if any).  Caller can use this to tile a
    transcription without overlap."""
    raw = recognize_words(stream, vocab=vocab, max_gap=max_gap)
    by_start = {}
    for r in raw:
        s = r["start_idx"]
        if s not in by_start or r["score"] > by_start[s]["score"]:
            by_start[s] = r
    return sorted(by_start.values(),
                  key=lambda r: r["t_start_sec"])


def greedy_transcribe(stream: List[Dict],
                       vocab: Dict[str, List[str]] = None,
                       max_gap: int = 1) -> List[Dict]:
    """Greedy left-to-right transcription: at each unconsumed stream
    position pick the longest highest-scoring word match and advance
    past it.  Returns the chosen sequence (a candidate sentence)."""
    raw = recognize_words(stream, vocab=vocab, max_gap=max_gap)
    raw.sort(key=lambda r: (r["start_idx"],
                             -len(r["target_pattern"]),
                             -r["score"]))
    chosen = []
    cursor = 0
    n = len(stream) if stream else 0
    while cursor < n:
        best = None
        for r in raw:
            if r["start_idx"] < cursor:
                continue
            if r["start_idx"] > cursor:
                break
            if best is None or len(r["target_pattern"]) > len(best["target_pattern"]) \
                    or (len(r["target_pattern"]) == len(best["target_pattern"])
                        and r["score"] > best["score"]):
                best = r
        if best is None:
            cursor += 1
            continue
        chosen.append(best)
        cursor = best["end_idx"] + 1
    return chosen


if __name__ == "__main__":
    # Smoke test: a synthetic phoneme stream that should produce
    # 'cat', 'see', 'a', 'dog'.
    stream = [
        {"t_offset_sec": 0.0, "duration_sec": 0.15, "key": "phoneme:k"},
        {"t_offset_sec": 0.15, "duration_sec": 0.15, "key": "phoneme:ae"},
        {"t_offset_sec": 0.30, "duration_sec": 0.15, "key": "phoneme:t"},
        {"t_offset_sec": 1.00, "duration_sec": 0.15, "key": "phoneme:s"},
        {"t_offset_sec": 1.15, "duration_sec": 0.15, "key": "phoneme:i"},
        {"t_offset_sec": 2.00, "duration_sec": 0.15, "key": "phoneme:V"},
        {"t_offset_sec": 3.00, "duration_sec": 0.15, "key": "phoneme:d"},
        {"t_offset_sec": 3.15, "duration_sec": 0.15, "key": "phoneme:O"},
        {"t_offset_sec": 3.30, "duration_sec": 0.15, "key": "phoneme:g"},
    ]
    matches = recognize_words(stream)
    print(f"raw recognitions: {len(matches)}")
    for r in matches[:20]:
        print(f"  {r['t_start_sec']:5.2f}-{r['t_end_sec']:5.2f}  "
              f"word={r['word']:8} score={r['score']:.2f}  "
              f"keys={r['matched_keys']}")
    print()
    print("greedy transcription:")
    g = greedy_transcribe(stream)
    print("  ", " ".join(r["word"] for r in g))
