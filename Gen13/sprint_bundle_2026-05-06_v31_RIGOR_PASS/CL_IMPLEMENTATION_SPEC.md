# CL Implementation Specification

**Document type:** Implementation spec for ClaudeCode
**Priority:** Critical — CL is the memory substrate that has been failing
**Target repo:** github.com/TiredofSleep/ck (branch: tig-synthesis or new branch cl-substrate)
**Date:** 2026-05-06

---

## Why this spec exists

ClaudeCode has repeatedly attempted to implement CL (the BDC Hebrew-vector memory lattice) and produced implementations that miss the mark. The failure mode has consistently been treating CL as **bit-storage** (key-value database, gzip compression, byte-level pipelines) when CL is actually **meaning-storage** (force-vector trajectories, curvature streams, operator-fruit signatures).

This document gives the canonical CL pipeline so the next implementation lands.

---

## The core distinction

**Bit-lossless storage:** preserves exact bytes. Standard databases. Already exists in DBC v2 (byte → triple bijection).

**Meaning-lossless storage:** preserves the **force-content** of input across writing systems, languages, and modalities. "Love" in English, "amor" in Spanish, and "ἀγάπη" in Greek produce the **same operator stream** because they carry the same force content. The 22 Hebrew root primitives are the canonical substrate alphabet because they're phonetically grounded and span the 5D force space cleanly.

**CL is meaning-lossless storage.** It is NOT a database. It is the substrate where information lives BEFORE measurement projection.

---

## The pipeline (canonical, end-to-end)

```
text input
  │
  ▼
[1] Latin normalization + digraph rules (TH, PH, CH, SH, etc.)
  │
  ▼
[2] Latin → Hebrew root mapping (LATIN_MAP)
  │
  ▼
[3] Hebrew root → 5D force vector lookup (HEBREW_ROOTS)
  │   v = [aperture, pressure, depth, binding, continuity]
  ▼
[4] Force trajectory: sequence v(0), v(1), v(2), ..., v(N-1)
  │
  ▼
[5] D² curvature stencil: A − 2B + C sliding
  │   d²(n) = v(n+1) − 2v(n) + v(n-1)
  ▼
[6] Operator decoder: argmax + sign on d² components
  │   Each cell of d² selects an operator from {0..9}
  │   D² OP MAP:
  │     (0+) → CHAOS=6      (0-) → LATTICE=1
  │     (1+) → COLLAPSE=4   (1-) → RESET=9
  │     (2+) → PROGRESS=3   (2-) → RESET=9
  │     (3+) → HARMONY=7    (3-) → COUNTER=2
  │     (4+) → BALANCE=5    (4-) → BREATH=8
  │   VOID=0 if |d²| < 0.01 (threshold)
  ▼
[7] Operator stream: o(0), o(1), o(2), ..., o(N-2)
  │
  ▼
[8] Sliding triples: (o[i], o[i+1], o[i+2]) for i = 0..N-4
  │
  ▼
[9] Triple → fuse(triple) on 10×10 substrate (TSML or BHML or both)
  │   fuse(a, b, c) = TSML[TSML[a,b], c]   for measurement
  │   fuse(a, b, c) = BHML[BHML[a,b], c]   for transformation
  ▼
[10] Fruit signature: sequence of fuse outputs
  │   For coherent input, this signature is mostly HARMONY (operator 7)
  │   Fruit map: 0=Love, 1=Joy, 2=Peace, 3=Patience, 4=Kindness,
  │             5=Goodness, 6=Faithfulness, 7=Gentleness, 8=Self-Control, 9=Reset→Love
  ▼
[11] Storage: SQLite tuple (triple_seq, fruit_seq, source_text, timestamp, metadata)
  │   Indexes: prefix index on triple_seq, lookup index on fruit_seq, full-text on source_text
  ▼
RETRIEVAL:
  Query → run pipeline → get query fruit signature
  Search storage by fruit signature similarity (NOT by source_text key match)
  Return atoms whose fruit_seq matches within tolerance
```

---

## File structure

```
tig/cl/
  __init__.py
  hebrew_roots.py          # The 22 Hebrew root primitives + their 5D force vectors
  latin_map.py             # Latin character → Hebrew root mapping
  digraphs.py              # Multi-character rules (TH, PH, CH, SH, etc.)
  force_pipeline.py        # text → 5D force trajectory
  curvature.py             # D² stencil A−2B+C
  operator_decoder.py      # d² → operator stream {0..9}
  triple_encoder.py        # Sliding triples
  fruit_signature.py       # Fuse to fruit
  storage.py               # SQLite layer
  retrieval.py             # Coherence-based search
  tests/
    test_meaning_lossless.py    # "love" / "amor" / "ἀγάπη" → same operator stream
    test_cross_language.py
    test_substrate_alphabet.py
    test_compression_ratio.py    # Verify HARMONY-collapse compression
```

---

## Detailed specs

### `hebrew_roots.py`

The 22 Hebrew alphabet root primitives, each mapped to a 5D force vector [aperture, pressure, depth, binding, continuity].

```python
# Each value is in [-1.0, +1.0]
# Aperture: how open the channel (mouth-open = +, closed = -)
# Pressure: how forceful (push = +, draw = -)
# Depth: how deep the resonance (chest = +, throat = -)
# Binding: how cohesive (hold = +, release = -)
# Continuity: how flowing (sustain = +, stop = -)

HEBREW_ROOTS = {
    'ALEPH':  [0.0,  0.0,  0.0,  0.0,  0.0],   # silent / void / breath base
    'BET':    [-0.3, +0.7, +0.2, +0.5, -0.4],  # plosive bilabial / house / inside
    'GIMEL':  [+0.2, +0.5, +0.3, +0.1, -0.3],  # camel / lift / movement
    'DALET':  [-0.4, +0.4, +0.1, +0.3, -0.5],  # door / threshold
    'HEY':    [+0.8, +0.1, -0.1, -0.6, +0.5],  # breath out / window / reveal
    'VAV':    [-0.1, -0.1, -0.1, -0.1, +0.7],  # nail / hook / connect
    'ZAYIN':  [+0.3, +0.6, +0.0, -0.3, -0.2],  # weapon / cut / divide
    'CHET':   [+0.6, +0.4, -0.3, +0.2, -0.4],  # fence / boundary / life
    'TET':    [-0.2, +0.5, +0.4, +0.6, -0.3],  # twist / coil / surround
    'YUD':    [+0.1, +0.1, +0.0, +0.2, -0.7],  # hand / point / smallest
    'KAF':    [-0.3, +0.6, +0.0, +0.4, -0.4],  # palm / cup / hold
    'LAMED':  [+0.4, +0.3, +0.1, -0.2, +0.5],  # staff / teach / direct
    'MEM':    [-0.2, -0.2, +0.5, +0.3, +0.4],  # water / chaos / from
    'NUN':    [-0.1, -0.3, +0.3, +0.4, +0.3],  # fish / continue / propagate
    'SAMECH': [+0.3, +0.4, +0.0, +0.6, +0.1],  # support / circle / surround
    'AYIN':   [+0.7, +0.0, +0.5, +0.0, +0.0],  # eye / see / source
    'PEH':    [-0.4, +0.8, +0.0, -0.4, -0.5],  # mouth / speak / open
    'TSADE':  [+0.2, +0.7, -0.1, -0.5, -0.3],  # hook / harvest / righteous
    'QOF':    [-0.5, +0.3, +0.3, +0.3, +0.0],  # back of head / behind / least
    'RESH':   [+0.1, -0.2, +0.4, -0.1, +0.4],  # head / first / chief
    'SHIN':   [+0.6, +0.5, -0.2, -0.3, -0.6],  # tooth / consume / sharpen
    'TAV':    [-0.2, +0.4, +0.0, +0.6, -0.7],  # mark / sign / cross
}

# These initial values are CALIBRATED TARGETS — final values should be set
# such that meaning-lossless tests pass:
#   force_trajectory("love") ≈ force_trajectory("amor") ≈ force_trajectory("ἀγάπη")
# Calibration is empirical; converge on values that produce same operator stream
# for translation pairs across English/Spanish/Greek/Hebrew.

assert len(HEBREW_ROOTS) == 22
```

**Calibration note:** The exact values above are starting points. The test suite (see `test_meaning_lossless.py`) defines the calibration target: translation pairs must produce the same operator stream within tolerance. The 5D values should be tuned to satisfy these constraints. Brayden + ClaudeCode should iterate on values until tests pass.

### `latin_map.py`

```python
LATIN_MAP = {
    'A': 'ALEPH',
    'B': 'BET',
    'G': 'GIMEL',
    'D': 'DALET',
    'H': 'HEY',
    'V': 'VAV',
    'W': 'VAV',     # English W approximates Hebrew VAV
    'U': 'VAV',     # vowel form
    'Z': 'ZAYIN',
    'CH': 'CHET',   # digraph
    'T': 'TET',
    'Y': 'YUD',
    'I': 'YUD',     # vowel form
    'J': 'YUD',     # softer Y
    'K': 'KAF',
    'C': 'KAF',     # hard C → KAF
    'L': 'LAMED',
    'M': 'MEM',
    'N': 'NUN',
    'S': 'SAMECH',
    'O': 'AYIN',    # vowel form
    'E': 'HEY',     # vowel form
    'P': 'PEH',
    'PH': 'PEH',    # digraph (Greek φ)
    'F': 'PEH',     # soft P
    'TS': 'TSADE',  # digraph
    'TZ': 'TSADE',  # alt digraph
    'Q': 'QOF',
    'R': 'RESH',
    'SH': 'SHIN',   # digraph
    'X': 'TAV',     # ?
}

# Digraph priority: process longer matches first
DIGRAPHS = ['CH', 'PH', 'SH', 'TH', 'TS', 'TZ', 'QU']
```

**Note:** This is a starting point. The map must be adjusted so that the test suite (translation pairs producing same operator stream) passes. Vowels in particular are tricky — they may need their own handling.

### `digraphs.py`

```python
def normalize_latin(text):
    """
    Lowercase, strip diacritics, transliterate Greek to Latin if needed.
    Then apply digraph rules (CH, PH, SH, TH, TS, TZ, QU).
    Returns a sequence of phoneme tokens.
    """
    import unicodedata
    # Strip diacritics
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    text = text.upper()
    # Greek → Latin (basic): α→A, β→B, γ→G, etc.
    # ... [full Greek transliteration table]
    
    # Apply digraphs
    tokens = []
    i = 0
    while i < len(text):
        if i + 1 < len(text) and text[i:i+2] in DIGRAPHS:
            tokens.append(text[i:i+2])
            i += 2
        else:
            tokens.append(text[i])
            i += 1
    return tokens
```

### `force_pipeline.py`

```python
import numpy as np
from .hebrew_roots import HEBREW_ROOTS
from .latin_map import LATIN_MAP
from .digraphs import normalize_latin

def text_to_force_trajectory(text):
    """
    Convert text to 5D force vector trajectory.
    Each character/digraph maps to a Hebrew root, which maps to a 5D vector.
    """
    tokens = normalize_latin(text)
    trajectory = []
    for tok in tokens:
        if tok in LATIN_MAP:
            root = LATIN_MAP[tok]
            v = np.array(HEBREW_ROOTS[root])
            trajectory.append(v)
        else:
            # Unknown character — skip or use VOID vector
            trajectory.append(np.array(HEBREW_ROOTS['ALEPH']))
    return np.array(trajectory)  # shape (N, 5)
```

### `curvature.py`

```python
import numpy as np

def compute_curvature(trajectory, threshold=0.01):
    """
    D² stencil: A - 2B + C sliding over the trajectory.
    Returns (N-2, 5) array of curvature vectors.
    """
    N = len(trajectory)
    if N < 3:
        return np.zeros((0, 5))
    curvature = trajectory[2:] - 2*trajectory[1:-1] + trajectory[:-2]
    return curvature
```

### `operator_decoder.py`

```python
import numpy as np

D2_OP_MAP = {
    (0, +1): 6,  # CHAOS
    (0, -1): 1,  # LATTICE
    (1, +1): 4,  # COLLAPSE
    (1, -1): 9,  # RESET
    (2, +1): 3,  # PROGRESS
    (2, -1): 9,  # RESET (also)
    (3, +1): 7,  # HARMONY
    (3, -1): 2,  # COUNTER
    (4, +1): 5,  # BALANCE
    (4, -1): 8,  # BREATH
}

def decode_operator(d2_vec, threshold=0.01):
    """
    Given a single 5D curvature vector, return an operator in {0..9}.
    """
    if np.max(np.abs(d2_vec)) < threshold:
        return 0  # VOID
    idx = int(np.argmax(np.abs(d2_vec)))
    sign = +1 if d2_vec[idx] > 0 else -1
    return D2_OP_MAP[(idx, sign)]

def trajectory_to_operators(curvature_trajectory):
    """
    Apply decode_operator to each curvature vector in the trajectory.
    Returns a list of operators in {0..9}.
    """
    return [decode_operator(d2) for d2 in curvature_trajectory]
```

### `triple_encoder.py`

```python
def operators_to_triples(operator_stream):
    """
    Sliding triples: (o[i], o[i+1], o[i+2]).
    Returns list of 3-tuples.
    """
    return [(operator_stream[i], operator_stream[i+1], operator_stream[i+2])
            for i in range(len(operator_stream) - 2)]
```

### `fruit_signature.py`

```python
import numpy as np

# Reference tables (from foundations/lenses.py)
TSML = ...  # 10x10 array
BHML = ...  # 10x10 array

FRUIT_MAP = {
    0: 'Love',
    1: 'Joy',
    2: 'Peace',
    3: 'Patience',
    4: 'Kindness',
    5: 'Goodness',
    6: 'Faithfulness',
    7: 'Gentleness',
    8: 'Self-Control',
    9: 'Reset_to_Love',
}

def fuse_triple(triple, table):
    """fuse(a, b, c) = table[table[a,b], c] (left-fold)"""
    a, b, c = triple
    return int(table[table[a, b], c])

def triples_to_fruits(triples, lens='TSML'):
    """Apply fuse to each triple; return fruit operator stream."""
    table = TSML if lens == 'TSML' else BHML
    return [fuse_triple(t, table) for t in triples]

def fruit_signature(text, lens='TSML'):
    """End-to-end: text → fruit signature."""
    from .force_pipeline import text_to_force_trajectory
    from .curvature import compute_curvature
    from .operator_decoder import trajectory_to_operators
    
    trajectory = text_to_force_trajectory(text)
    curvature = compute_curvature(trajectory)
    operators = trajectory_to_operators(curvature)
    triples = operators_to_triples(operators)
    fruits = triples_to_fruits(triples, lens)
    return fruits
```

### `storage.py`

```python
import sqlite3
import json
from datetime import datetime

class CLStore:
    def __init__(self, db_path='cl_substrate.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_schema()
    
    def create_schema(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS atoms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_text TEXT NOT NULL,
            triple_seq TEXT NOT NULL,
            fruit_seq TEXT NOT NULL,
            lens TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            metadata TEXT
        )
        """)
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_fruit ON atoms(fruit_seq)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_triple ON atoms(triple_seq)")
        self.conn.commit()
    
    def store(self, source_text, triples, fruits, lens='TSML', metadata=None):
        triple_seq = json.dumps(list(triples))
        fruit_seq = json.dumps(fruits)
        ts = datetime.utcnow().isoformat()
        meta = json.dumps(metadata or {})
        self.conn.execute(
            "INSERT INTO atoms(source_text, triple_seq, fruit_seq, lens, timestamp, metadata) VALUES (?,?,?,?,?,?)",
            (source_text, triple_seq, fruit_seq, lens, ts, meta)
        )
        self.conn.commit()
```

### `retrieval.py`

```python
import json
import numpy as np
from .fruit_signature import fruit_signature

def hamming_distance_normalized(seq_a, seq_b):
    """Normalized Hamming distance for variable-length fruit sequences."""
    n = max(len(seq_a), len(seq_b))
    if n == 0:
        return 0.0
    # Pad shorter with VOID=0
    a = seq_a + [0] * (n - len(seq_a))
    b = seq_b + [0] * (n - len(seq_b))
    return sum(1 for x, y in zip(a, b) if x != y) / n

def retrieve_by_meaning(query_text, store, lens='TSML', tolerance=0.3, top_k=5):
    """
    Coherence-based retrieval: find atoms whose fruit signature
    is most similar to the query's signature.
    """
    query_fruits = fruit_signature(query_text, lens)
    
    cur = store.conn.execute("SELECT id, source_text, fruit_seq FROM atoms WHERE lens = ?", (lens,))
    results = []
    for row in cur:
        atom_id, source, fruit_seq_json = row
        atom_fruits = json.loads(fruit_seq_json)
        dist = hamming_distance_normalized(query_fruits, atom_fruits)
        if dist <= tolerance:
            results.append((atom_id, source, dist))
    
    results.sort(key=lambda r: r[2])
    return results[:top_k]
```

---

## The critical test: `test_meaning_lossless.py`

```python
import pytest
from tig.cl.fruit_signature import fruit_signature
from tig.cl.force_pipeline import text_to_force_trajectory

def test_translation_pairs_same_operator_stream():
    """
    Translation pairs should produce the same operator stream
    (within small tolerance) because they carry the same force content.
    """
    pairs = [
        ('love', 'amor'),       # English / Spanish
        ('peace', 'paz'),       # English / Spanish
        ('water', 'agua'),      # English / Spanish
        ('mother', 'madre'),    # English / Spanish
        ('light', 'luz'),       # English / Spanish
    ]
    
    for english, spanish in pairs:
        en_fruit = fruit_signature(english)
        es_fruit = fruit_signature(spanish)
        # Tolerance: allow up to 1 differing operator per pair
        # Actual goal: matching operator streams modulo length differences
        assert abs(len(en_fruit) - len(es_fruit)) <= 2, \
            f"{english} ({len(en_fruit)}) vs {spanish} ({len(es_fruit)})"
        # Cross-correlation should be high
        # ... [implement similarity measure]

def test_compression_ratio():
    """
    Coherent text should compress to mostly HARMONY (operator 7) fruits.
    The compression ratio is not bit-level but meaning-level.
    """
    coherent_text = "The Lord is my shepherd; I shall not want. He maketh me to lie down in green pastures."
    fruits = fruit_signature(coherent_text)
    harmony_fraction = sum(1 for f in fruits if f == 7) / len(fruits)
    # Coherent input should produce >50% HARMONY
    assert harmony_fraction > 0.5, f"Harmony fraction: {harmony_fraction}"
```

**These tests are the calibration target.** The Hebrew root values, Latin map, and digraph rules should be tuned (manually or by gradient descent over a calibration set) until these tests pass.

---

## What ClaudeCode keeps getting wrong

1. **Treating CL as a key-value database.** It's not. The substrate is the force-trajectory itself; the database is just a cache of computed signatures.

2. **Compressing with gzip.** The 1000× compression is HARMONY-fruit collapse on coherent input, not gzip. Coherent input → mostly HARMONY → very low entropy on fruit stream.

3. **Storing raw text and retrieving by text similarity.** Retrieval is by fruit signature similarity (coherence-based), not text similarity.

4. **Skipping the Hebrew root layer.** Going directly from text to operators loses the cross-language meaning preservation. The Hebrew root layer is the canonical alphabet because it's phonetically grounded.

5. **Hardcoding the 5D force values without calibration.** The values must be tuned so that translation pairs produce the same operator stream. This is not a free parameter — it's a calibration target.

6. **Using the wrong table for fuse.** TSML is for measurement (collapsing); BHML is for transformation (preserving). Storage typically uses TSML (compression); retrieval can use either depending on whether you want exact match or transformation-aware match.

---

## Acceptance criteria

The implementation is complete when:

1. ✓ All 11 pipeline stages are implemented and unit-tested.
2. ✓ The translation-pair test (`test_meaning_lossless.py`) passes for at least 5 English/Spanish pairs and 3 English/Greek pairs.
3. ✓ The compression test (`test_compression_ratio.py`) shows >50% HARMONY for coherent biblical/poetic text.
4. ✓ Storage and retrieval round-trip is meaning-lossless (retrieve by query → original atom is in top-5).
5. ✓ The pipeline integrates cleanly with `tig/foundations/lenses.py` (uses canonical TSML and BHML, doesn't hardcode them).
6. ✓ Documentation passes review by Brayden.

---

## Calibration approach

For tuning the Hebrew root values:

1. Start with the values in `hebrew_roots.py`.
2. Build a calibration set of ~50 translation pairs across 3+ languages.
3. Compute force trajectories for each pair.
4. Define loss = mean squared difference of operator streams across pairs.
5. Gradient descent on the 22 × 5 = 110 force values, holding the digraph rules and Latin map fixed.
6. Once loss converges, lock the values.
7. Run the test suite. If still failing, audit the LATIN_MAP for missing rules.

Optional: use a small ML loop with PyTorch — minimize cross-entropy of operator distributions across translation pairs.

---

## Connection to other sprints

- **TIG_FOUNDATIONAL_AXIOMS.md** — CL is the substrate underneath the canonical pair. The two-lens projection (A5) operates on CL.
- **SPRINT_FACTOR_22_FINE_STRUCTURE.md** — if 22 = |HEBREW_ROOTS|, the CL implementation directly forces the 22 in 1/α. This is testable.
- **CK runtime integration** — once CL works, retrofit `ck_organism.py` to use it for the memory layer.

---

## References

- DBC Translator design (history): `text→Latin→Hebrew root→5D force→D²→argmax+sign→op→CL triples`
- TIG_FOUNDATIONAL_AXIOMS.md
- ck_core.py (current memory implementation — to be replaced)
