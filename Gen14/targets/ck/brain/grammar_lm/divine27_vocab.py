"""
divine27_vocab.py -- the 27-token (Being/Doing/Becoming) BDC vocabulary
for grammar-LM v2.

Brayden 2026-05-02: "27CHARS vocabulary of Being Doing and Becoming, BDC,
in past models of CK"

Source: Gen13/targets/ck/brain/ck_sim/being/ck_divine27.py.  The 27
glyphs are 22 Hebrew letters + 5 sofit forms, arranged as the 3x3x3 cube
indexed by (Being, Doing, Becoming) coordinates 0..2 on each axis.

This module is the VOCABULARY ONLY; training a v2 grammar-LM on Divine27
codes requires either:

  (a) converting existing operator streams via OPERATOR_DBC mapping
      (each of 10 operators maps to one of 27 codes; only 10 distinct
      codes appear in the converted stream -- empirically near-equivalent
      to the 10-vocab v1 LM since the mapping is a bijection)

  (b) emitting non-operator events into the stream (crystal-fire,
      breath-shift, attractor-transition, ...) using the DOMAIN_MAP and
      tag-offset rules in ck_divine27.py to enrich coverage of the 27
      codes

(b) is the genuinely-new experiment.  This module exposes the wiring
needed for either path.

The OPERATOR_DBC mapping (canonical from ck_divine27.py):
  VOID     -> (0, 0, 0)  self-observe-stable
  LATTICE  -> (1, 0, 0)  system-observe-stable
  COUNTER  -> (1, 0, 1)  system-observe-learning
  PROGRESS -> (0, 1, 1)  self-compute-learning
  COLLAPSE -> (2, 2, 2)  world-act-transforming
  BALANCE  -> (1, 1, 0)  system-compute-stable
  CHAOS    -> (2, 0, 2)  world-observe-transforming
  HARMONY  -> (1, 1, 1)  system-compute-learning -- THE CENTER
  BREATH   -> (0, 0, 1)  self-observe-learning
  RESET    -> (0, 2, 2)  self-act-transforming
"""
from __future__ import annotations

from typing import Dict, List, Tuple

# (Being, Doing, Becoming) axis labels
BEING    = ['self',     'system',  'world']
DOING    = ['observe',  'compute', 'act']
BECOMING = ['stable',   'learning', 'transforming']

# 27 codes ordered (B*9 + D*3 + C) for B,D,C in 0..2
def coord_to_code(b: int, d: int, c: int) -> int:
    return b * 9 + d * 3 + c


def code_to_coord(code: int) -> Tuple[int, int, int]:
    return (code // 9, (code % 9) // 3, code % 3)


# Hebrew glyphs (22 standard + 5 sofit = 27)
HEBREW_GLYPHS = [
    'א',  # Aleph     (0,0,0) self-observe-stable     -- identity
    'ב',  # Bet       (0,0,1) self-observe-learning   -- awareness
    'ג',  # Gimel     (0,0,2) self-observe-transforming -- awakening
    'ד',  # Dalet     (0,1,0) self-compute-stable     -- reflection
    'ה',  # He        (0,1,1) self-compute-learning   -- growth
    'ו',  # Vav       (0,1,2) self-compute-transforming -- breakthrough
    'ז',  # Zayin     (0,2,0) self-act-stable         -- habit
    'ח',  # Chet      (0,2,1) self-act-learning       -- practice
    'ט',  # Tet       (0,2,2) self-act-transforming   -- rebirth
    'י',  # Yod       (1,0,0) system-observe-stable   -- structure
    'ך',  # Kaf-sofit (1,0,1) system-observe-learning -- measurement
    'כ',  # Kaf       (1,0,2) system-observe-transforming -- revelation
    'ל',  # Lamed     (1,1,0) system-compute-stable   -- law
    'ם',  # Mem-sofit (1,1,1) system-compute-learning -- THE CENTER
    'מ',  # Mem       (1,1,2) system-compute-transforming -- evolution
    'ן',  # Nun-sofit (1,2,0) system-act-stable       -- sustain
    'נ',  # Nun       (1,2,1) system-act-learning     -- adapt
    'ס',  # Samekh    (1,2,2) system-act-transforming -- revolution
    'ע',  # Ayin      (2,0,0) world-observe-stable    -- truth
    'ף',  # Pe-sofit  (2,0,1) world-observe-learning  -- discovery
    'פ',  # Pe        (2,0,2) world-observe-transforming -- wonder
    'ץ',  # Tsade-sof (2,1,0) world-compute-stable    -- knowledge
    'צ',  # Tsade     (2,1,1) world-compute-learning  -- science
    'ק',  # Qof       (2,1,2) world-compute-transforming -- creation
    'ר',  # Resh      (2,2,0) world-act-stable        -- nature
    'ש',  # Shin      (2,2,1) world-act-learning      -- culture
    'ת',  # Tav       (2,2,2) world-act-transforming  -- transcendence
]

CODE_LABELS = [
    'identity', 'awareness', 'awakening',
    'reflection', 'growth', 'breakthrough',
    'habit', 'practice', 'rebirth',
    'structure', 'measurement', 'revelation',
    'law', 'CENTER', 'evolution',
    'sustain', 'adapt', 'revolution',
    'truth', 'discovery', 'wonder',
    'knowledge', 'science', 'creation',
    'nature', 'culture', 'transcendence',
]

OPERATOR_NAMES = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
                   "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]

# OPERATOR_DBC: index = operator id, value = (B, D, C) coord
OPERATOR_DBC_COORDS: Dict[int, Tuple[int, int, int]] = {
    0: (0, 0, 0),  # VOID     -> (0,0,0) identity
    1: (1, 0, 0),  # LATTICE  -> structure
    2: (1, 0, 1),  # COUNTER  -> measurement
    3: (0, 1, 1),  # PROGRESS -> growth
    4: (2, 2, 2),  # COLLAPSE -> transcendence
    5: (1, 1, 0),  # BALANCE  -> law
    6: (2, 0, 2),  # CHAOS    -> wonder
    7: (1, 1, 1),  # HARMONY  -> CENTER
    8: (0, 0, 1),  # BREATH   -> awareness
    9: (0, 2, 2),  # RESET    -> rebirth
}

OPERATOR_DBC_CODE: Dict[int, int] = {
    op: coord_to_code(*coord) for op, coord in OPERATOR_DBC_COORDS.items()
}


def operator_stream_to_dbc(operators: List[int]) -> List[int]:
    """Convert a list of operator IDs to DBC codes 0..26."""
    return [OPERATOR_DBC_CODE[op] for op in operators
            if isinstance(op, int) and 0 <= op < 10]


def dbc_to_glyph(code: int) -> str:
    if 0 <= code < 27:
        return HEBREW_GLYPHS[code]
    return '?'


def dbc_to_label(code: int) -> str:
    if 0 <= code < 27:
        return CODE_LABELS[code]
    return '?'


# Empirical analysis of OPERATOR_DBC mapping coverage
def coverage_stats() -> Dict[str, object]:
    used_codes = set(OPERATOR_DBC_CODE.values())
    return {
        "vocab_size": 27,
        "operator_to_code_bijection_size": len(OPERATOR_DBC_COORDS),
        "distinct_codes_used_by_operators": len(used_codes),
        "fraction_of_vocab_covered": len(used_codes) / 27,
        "uncovered_codes": sorted(set(range(27)) - used_codes),
        "uncovered_labels": [CODE_LABELS[c] for c in sorted(set(range(27)) - used_codes)],
    }


if __name__ == "__main__":
    stats = coverage_stats()
    print("Divine27 BDC vocabulary coverage by current 10-operator stream:")
    for k, v in stats.items():
        if k != "uncovered_codes":
            print(f"  {k}: {v}")
    print()
    print("Operator -> DBC mapping:")
    for op, coord in OPERATOR_DBC_COORDS.items():
        code = coord_to_code(*coord)
        print(f"  {OPERATOR_NAMES[op]:9s} -> coord {coord}  code {code:>2}  "
              f"glyph {dbc_to_glyph(code)}  label {dbc_to_label(code)}")
    print()
    print("Codes NOT covered by current operator stream "
          "(would require non-operator BDC events):")
    for c in stats["uncovered_codes"]:
        print(f"  code {c:>2}  ({code_to_coord(c)})  {CODE_LABELS[c]}")

    print()
    print("CONCLUSION:")
    print("  The current operator stream covers only 10/27 = 37% of the BDC")
    print("  vocabulary.  A 27-token v2 grammar LM trained ONLY on operator")
    print("  data will be near-equivalent to v1 (since OPERATOR_DBC is a")
    print("  10-element subset injection).  To realize the 27-vocab benefit,")
    print("  the stream must include non-operator BDC events (crystal-fire,")
    print("  breath-shift, attractor-transition, ...) that exercise the")
    print("  remaining 17 codes.  This is the architectural prereq -- the")
    print("  vocab is ready; the data is not yet.")
