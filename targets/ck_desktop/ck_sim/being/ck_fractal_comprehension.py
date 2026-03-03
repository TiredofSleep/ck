# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_fractal_comprehension.py -- Fractal Comprehension Engine
============================================================
Operator: COUNTER (2) -- CK decomposes what he receives.

I is structure. O is flow.
Those combine to make letters and geometries we call letters.
Then those arrangements form arrangements form arrangements...

The recursive comprehension chain:
  Level 0: Glyph Force     -- I/O decomposition per character
  Level 1: Letter Pairs    -- geometry relationships
  Level 2: Curvature       -- D2 + boundary detection (structure reset)
  Level 3: Word Interior   -- core/tail/fuse from letter-level geometry
  Level 4: Word Identity   -- word as whole (fuse = identity operator)
  Level 5: Word Relations  -- pair compositions + phrase boundaries
  Level 6: Triadic Becomings -- being->doing->becoming progressions
  Level 7+: Recursive      -- each grouping becomes input for next level

At EVERY level: separate structure from flow, compose via CL.
CL(structure, flow) = fuse = this level's identity operator.
The fuse becomes input to the next level.

CK doesn't just READ text. He COMPREHENDS it fractally.
Then comprehension operators feed his voice -- so he RESPONDS to content,
not just sits in his HARMONY basin.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

from typing import List, Optional, Tuple
from dataclasses import dataclass, field

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES, CL, compose
)
from ck_sim.ck_sim_d2 import (
    D2Pipeline, FORCE_LUT_FLOAT, D2_OP_MAP, soft_classify_d2,
    classify_force_d1
)


# ================================================================
#  I/O DECOMPOSITION: Structure and Flow from 5D Force Vectors
# ================================================================
#
# The 5 dimensions of each Hebrew root force vector:
#   dim 0: aperture    (opening/closing)     -> STRUCTURE
#   dim 1: pressure    (force of articulation) -> STRUCTURE
#   dim 2: depth       (place, front/back)   -> BRIDGE
#   dim 3: binding     (connection to adjacent) -> FLOW
#   dim 4: continuity  (sustained vs plosive)   -> FLOW
#
# Structure (I): |aperture| + |pressure| -- how much force is exerted
# Flow (O):      |binding| + |continuity| -- how much connection/sustaining
#
# At Level 0, each letter decomposes into:
#   structure_op: dominant structure dimension -> operator via D2_OP_MAP
#   flow_op:      dominant flow dimension -> operator via D2_OP_MAP
#   fuse = CL[structure_op][flow_op]
#
# This is the I/O principle applied to each glyph.

# Operator classification by DBC (Being/Doing/Becoming) axis
# Used for triadic becoming detection at Level 6
_BEING_OPS = {VOID, LATTICE, HARMONY}      # States of existence
_DOING_OPS = {COUNTER, PROGRESS, COLLAPSE, BALANCE}  # Actions
_BECOMING_OPS = {CHAOS, BREATH, RESET}     # Transitions


# ================================================================
#  DATA STRUCTURES
# ================================================================

@dataclass
class GlyphForce:
    """Level 0: Single character's structure/flow decomposition."""
    char: str
    force: tuple          # 5D force vector (apt, press, depth, bind, cont)
    structure: float      # |aperture| + |pressure|
    flow: float           # |binding| + |continuity|
    depth: float          # |depth|
    structure_op: int     # Operator from dominant structure dimension
    flow_op: int          # Operator from dominant flow dimension
    fuse: int             # CL[structure_op][flow_op]
    io_ratio: float       # structure / (structure + flow)


@dataclass
class FractalUnit:
    """A unit at any level of the fractal comprehension."""
    level: int
    structure_op: int     # What's stable/reinforcing at this level
    flow_op: int          # What's changing/transitioning at this level
    fuse: int             # CL[structure_op][flow_op] = identity
    io_ratio: float       # structure weight / (structure + flow)
    raw: str              # Source text this unit represents
    is_boundary: bool     # True = structure reset point


@dataclass
class ComprehensionResult:
    """Full fractal comprehension of a text."""
    levels: list          # List of lists: units at each level
    level_fuses: list     # One fuse per level (running CL composition)
    comprehension_ops: list  # Operator sequence from all levels
    dominant_op: int      # Most frequent comprehension operator
    structure_flow_balance: float  # Overall I/O ratio [0=pure flow, 1=pure structure]
    boundaries: int       # Total structure reset points
    becomings: int        # Total triadic progressions found
    depth: int            # How many levels were meaningful
    word_fuses: list      # Per-word fuse operators (for responsive voice)
    # ── D1 Generator Layer ──
    # D1 = first derivative (velocity/direction). Fires after 2 letters.
    # Generators run off D1 (the simple curve).
    # Complexity breeds from D2 (the curve of the curve).
    d1_generators: list = field(default_factory=list)   # Raw D1 ops per position
    word_d1_ops: list = field(default_factory=list)     # Per-word D1 dominant op
    d1_d2_harmony: float = 0.0   # Fraction of positions where CL(D1,D2)=HARMONY
    density_ratio: float = 0.0   # D2_mag / D1_mag -- complexity per generator step


# ================================================================
#  FRACTAL COMPREHENSION ENGINE
# ================================================================

class FractalComprehension:
    """
    Recursive fractal decomposition of text.

    Each level's output feeds the next level's input.
    At every level: separate structure from flow, compose via CL.
    The composition IS the unit's identity for the next level.
    """

    def __init__(self):
        self.max_depth = 10  # Max recursive levels beyond Level 6

    # ── Main entry point ──

    def comprehend(self, text: str) -> ComprehensionResult:
        """
        Full fractal comprehension of input text.

        Returns ComprehensionResult with operators at each level,
        ready to feed into CK's voice composition.
        """
        if not text or not text.strip():
            return ComprehensionResult(
                levels=[], level_fuses=[], comprehension_ops=[VOID],
                dominant_op=VOID, structure_flow_balance=0.5,
                boundaries=0, becomings=0, depth=0, word_fuses=[])

        all_levels = []
        level_fuses = []

        # Level 0: Glyph Forces
        glyphs = self._level_0_glyphs(text)
        all_levels.append(glyphs)
        l0_fuse = self._level_fuse([g.fuse for g in glyphs])
        level_fuses.append(l0_fuse)

        # Level 1: Letter Pair Relations
        pairs = self._level_1_pairs(glyphs)
        all_levels.append(pairs)
        if pairs:
            l1_fuse = self._level_fuse([p.fuse for p in pairs])
            level_fuses.append(l1_fuse)

        # Level 2: D2 Curvature (with boundary detection) + D1 generators
        curvatures, d1_generators, d1_d2_pairs, d1_mags, d2_mags = \
            self._level_2_curvatures(text)
        all_levels.append(curvatures)
        if curvatures:
            l2_fuse = self._level_fuse([c.fuse for c in curvatures])
            level_fuses.append(l2_fuse)

        # ── D1↔D2 metrics (generator vs complexity) ──
        # CL(D1, D2) = how generator meets complexity at each position
        d1_d2_harmony_count = 0
        for d1_op, d2_op in d1_d2_pairs:
            if CL[d1_op][d2_op] == HARMONY:
                d1_d2_harmony_count += 1
        d1_d2_harmony = (d1_d2_harmony_count / len(d1_d2_pairs)
                         if d1_d2_pairs else 0.0)

        # Density ratio: how much curvature per unit velocity
        avg_d1_mag = sum(d1_mags) / len(d1_mags) if d1_mags else 0.001
        avg_d2_mag = sum(d2_mags) / len(d2_mags) if d2_mags else 0.0
        density_ratio = avg_d2_mag / avg_d1_mag if avg_d1_mag > 0.001 else 0.0

        # Level 3: Word Internal Structure (histogram-based fuses)
        words = self._level_3_words(text, glyphs)
        all_levels.append(words)
        word_fuses_list = [w.fuse for w in words] if words else []
        if words:
            l3_fuse = self._level_fuse(word_fuses_list)
            level_fuses.append(l3_fuse)

        # Level 5: Word Relations (CL composition for interaction, not identity)
        word_rels = self._level_5_word_relations(words)
        all_levels.append(word_rels)
        if word_rels:
            l5_fuse = self._level_fuse([r.fuse for r in word_rels])
            level_fuses.append(l5_fuse)

        # Level 6: Triadic Becomings
        triads = self._level_6_triadic_becomings(words)
        all_levels.append(triads)
        if triads:
            l6_fuse = self._level_fuse([t.fuse for t in triads])
            level_fuses.append(l6_fuse)

        # Level 7+: Recursive grouping
        current_units = triads if triads else words
        for lvl in range(7, 7 + self.max_depth):
            if len(current_units) < 2:
                break
            grouped = self._recursive_group(current_units, lvl)
            if not grouped:
                break
            all_levels.append(grouped)
            g_fuse = self._level_fuse([g.fuse for g in grouped])
            level_fuses.append(g_fuse)
            current_units = grouped

        # ── Per-word D1 generators ──
        # Group D1 ops by word boundaries (same word positions as Level 3)
        word_d1_ops = []
        if d1_generators and words:
            # D1 fires once per letter pair. Approximate word boundaries
            # by splitting d1_generators proportional to word lengths.
            d1_idx = 0
            for w in text.split():
                w_letters = sum(1 for c in w if c.isalpha())
                # D1 fires for each pair = (letters - 1) ops per word
                n_d1 = max(0, w_letters - 1)
                word_d1 = d1_generators[d1_idx:d1_idx + n_d1]
                d1_idx += n_d1
                if word_d1:
                    # Most common D1 op = this word's generator identity
                    d1_counts = [0] * NUM_OPS
                    for op in word_d1:
                        d1_counts[op] += 1
                    word_d1_ops.append(
                        max(range(NUM_OPS), key=lambda i: d1_counts[i]))
                elif word_fuses_list and len(word_d1_ops) < len(word_fuses_list):
                    word_d1_ops.append(VOID)  # Too short for D1

        # ── Extract comprehension operators ──
        comprehension_ops = list(level_fuses)

        # Also include word-level fuses (they carry the most content info)
        if word_fuses_list:
            comprehension_ops.extend(word_fuses_list[:8])

        # Count total boundaries and becomings
        total_boundaries = sum(
            sum(1 for u in lvl_units if isinstance(u, FractalUnit) and u.is_boundary)
            for lvl_units in all_levels
            if lvl_units and isinstance(lvl_units[0], FractalUnit)
        )
        total_becomings = len(triads)

        # I/O balance
        if glyphs:
            avg_io = sum(g.io_ratio for g in glyphs) / len(glyphs)
        else:
            avg_io = 0.5

        # Dominant operator
        op_counts = [0] * NUM_OPS
        for op in comprehension_ops:
            if 0 <= op < NUM_OPS:
                op_counts[op] += 1
        dominant = max(range(NUM_OPS), key=lambda i: op_counts[i])

        return ComprehensionResult(
            levels=all_levels,
            level_fuses=level_fuses,
            comprehension_ops=comprehension_ops,
            dominant_op=dominant,
            structure_flow_balance=avg_io,
            boundaries=total_boundaries,
            becomings=total_becomings,
            depth=len(all_levels),
            word_fuses=word_fuses_list,
            d1_generators=d1_generators,
            word_d1_ops=word_d1_ops,
            d1_d2_harmony=d1_d2_harmony,
            density_ratio=density_ratio,
        )

    # ── Level 0: Glyph Force (I/O at letter level) ──

    def _level_0_glyphs(self, text: str) -> List[GlyphForce]:
        """Decompose each character into structure + flow operators.

        Fuse uses argmax of the FULL 5D force vector (not CL composition).
        CL has 73 harmonies and destroys content information.
        The raw force argmax preserves which dimension dominates:
          dim 0 (aperture)   -> CHAOS    = opening, expansion
          dim 1 (pressure)   -> COLLAPSE = force, compression
          dim 2 (depth)      -> PROGRESS = deepening
          dim 3 (binding)    -> HARMONY  = connection
          dim 4 (continuity) -> BALANCE  = sustaining
        """
        glyphs = []
        for ch in text:
            c = ch.lower()
            if c < 'a' or c > 'z':
                continue
            idx = ord(c) - ord('a')
            force = FORCE_LUT_FLOAT[idx]

            # Structure (I): aperture + pressure
            structure = force[0] + force[1]
            # Flow (O): binding + continuity
            flow = force[3] + force[4]
            # Depth: bridge
            depth_val = force[2]

            # Classify structure: which force dimension dominates?
            if force[0] >= force[1]:
                struct_op = D2_OP_MAP[0][0]  # CHAOS
            else:
                struct_op = D2_OP_MAP[1][0]  # COLLAPSE

            # Classify flow: which connection dimension dominates?
            if force[3] >= force[4]:
                flow_op = D2_OP_MAP[3][0]  # HARMONY
            else:
                flow_op = D2_OP_MAP[4][0]  # BALANCE

            # Fuse: argmax of FULL 5D force vector.
            # NOT CL composition (73-harmony absorbs everything).
            # The dominant dimension IS the glyph's identity.
            max_dim = 0
            max_val = 0.0
            for d in range(5):
                if force[d] > max_val:
                    max_val = force[d]
                    max_dim = d
            # All raw forces are positive, so use positive mapping
            fuse = D2_OP_MAP[max_dim][0]

            total = structure + flow
            io_ratio = structure / total if total > 0 else 0.5

            glyphs.append(GlyphForce(
                char=c, force=force, structure=structure, flow=flow,
                depth=depth_val, structure_op=struct_op, flow_op=flow_op,
                fuse=fuse, io_ratio=io_ratio))

        return glyphs

    # ── Level 1: Letter Pair Relations ──

    def _level_1_pairs(self, glyphs: List[GlyphForce]) -> List[FractalUnit]:
        """Relationships between adjacent letter geometries."""
        if len(glyphs) < 2:
            return []

        pairs = []
        for i in range(len(glyphs) - 1):
            a = glyphs[i]
            b = glyphs[i + 1]

            # Force difference: how does geometry CHANGE?
            delta = tuple(b.force[d] - a.force[d] for d in range(5))

            # Structure of relationship: change in structure dimensions
            delta_struct = abs(delta[0]) + abs(delta[1])
            # Flow of relationship: change in flow dimensions
            delta_flow = abs(delta[3]) + abs(delta[4])

            # Reinforcement: do they agree? (cosine similarity)
            dot = sum(a.force[d] * b.force[d] for d in range(5))
            mag_a = sum(v * v for v in a.force) ** 0.5
            mag_b = sum(v * v for v in b.force) ** 0.5
            reinforcement = dot / (mag_a * mag_b) if mag_a > 0 and mag_b > 0 else 0.0

            # When pair AGREES (high reinforcement): structure dominates
            # When pair DISAGREES (low reinforcement): flow dominates (tension)
            if reinforcement >= 0.7:
                # Agreement: structure is the shared identity
                struct_op = a.fuse  # What they share
                flow_op = b.fuse    # How they differ
            else:
                # Tension: the CHANGE is what matters
                # Classify the delta vector
                struct_op = self._classify_force_subspace(delta, 'structure')
                flow_op = self._classify_force_subspace(delta, 'flow')

            # Fuse: argmax of the relationship's dominant signal
            # (NOT CL -- 73 harmonies would absorb everything)
            if delta_struct >= delta_flow:
                fuse = struct_op
            else:
                fuse = flow_op
            total = delta_struct + delta_flow
            io_ratio = delta_struct / total if total > 0 else 0.5
            is_boundary = a.fuse != b.fuse  # Fuse change = relationship boundary

            pairs.append(FractalUnit(
                level=1, structure_op=struct_op, flow_op=flow_op,
                fuse=fuse, io_ratio=io_ratio,
                raw=a.char + b.char, is_boundary=is_boundary))

        return pairs

    # ── Level 2: D2 Curvature with Boundaries ──

    def _level_2_curvatures(self, text: str) -> tuple:
        """D2 curvature per position + boundary detection.

        Now also collects D1 (generator-level) operators.
        Returns (d2_units, d1_ops, d1_d2_pairs, d1_mags, d2_mags).
        """
        pipe = D2Pipeline()
        units = []
        d1_ops = []          # Raw D1 operators (generator level)
        d1_d2_pairs = []     # (D1_op, D2_op) for harmony measurement
        d1_mags = []         # D1 magnitudes (for density ratio)
        d2_mags = []         # D2 magnitudes (for density ratio)
        prev_op = -1

        for ch in text:
            c = ch.lower()
            if c < 'a' or c > 'z':
                continue
            idx = ord(c) - ord('a')
            pipe.feed_symbol(idx)

            # D1 fires after 2 letters (generator level)
            if pipe.d1_valid:
                d1_ops.append(pipe.d1_operator)
                d1_mags.append(pipe.d1_mag_float)

            # D2 fires after 3 letters (complexity level)
            if not pipe.valid:
                continue

            op = pipe.operator
            d2_vec = pipe.d2_float
            mag = pipe.d2_mag_float
            d2_mags.append(mag)

            # Record D1↔D2 pair for harmony measurement
            if pipe.d1_valid:
                d1_d2_pairs.append((pipe.d1_operator, pipe.operator))

            # Get soft classification for I/O decomposition of curvature
            soft = soft_classify_d2(d2_vec, mag)

            # Structure: weight in force-classified operators (CHAOS, LATTICE, COLLAPSE, VOID)
            struct_weight = soft[CHAOS] + soft[LATTICE] + soft[COLLAPSE] + soft[VOID]
            # Flow: weight in connection-classified operators (HARMONY, COUNTER, BALANCE, BREATH)
            flow_weight = soft[HARMONY] + soft[COUNTER] + soft[BALANCE] + soft[BREATH]

            # Structure op = highest structure-classified operator
            struct_ops = [(soft[CHAOS], CHAOS), (soft[LATTICE], LATTICE),
                         (soft[COLLAPSE], COLLAPSE), (soft[VOID], VOID)]
            struct_op = max(struct_ops, key=lambda x: x[0])[1]

            # Flow op = highest flow-classified operator
            flow_ops = [(soft[HARMONY], HARMONY), (soft[COUNTER], COUNTER),
                       (soft[BALANCE], BALANCE), (soft[BREATH], BREATH)]
            flow_op = max(flow_ops, key=lambda x: x[0])[1]

            fuse = CL[struct_op][flow_op]
            is_boundary = (op != prev_op and prev_op >= 0)
            prev_op = op

            total = struct_weight + flow_weight
            io_ratio = struct_weight / total if total > 0 else 0.5

            units.append(FractalUnit(
                level=2, structure_op=struct_op, flow_op=flow_op,
                fuse=fuse, io_ratio=io_ratio,
                raw=c, is_boundary=is_boundary))

        return units, d1_ops, d1_d2_pairs, d1_mags, d2_mags

    # ── Level 3: Word Internal Structure ──

    def _level_3_words(self, text: str, glyphs: List[GlyphForce]) -> List[FractalUnit]:
        """Build word-level units from letter-level decomposition."""
        words_text = text.split()
        if not words_text:
            return []

        word_units = []
        glyph_idx = 0

        for w in words_text:
            # Collect glyphs belonging to this word
            w_lower = ''.join(c for c in w.lower() if 'a' <= c <= 'z')
            n_letters = len(w_lower)
            if n_letters == 0:
                continue

            word_glyphs = glyphs[glyph_idx:glyph_idx + n_letters]
            glyph_idx += n_letters

            if not word_glyphs:
                continue

            # Word internal structure:
            # Core = most frequent glyph fuse (structure of the word)
            fuse_counts = [0] * NUM_OPS
            for g in word_glyphs:
                fuse_counts[g.fuse] += 1
            core_op = max(range(NUM_OPS), key=lambda i: fuse_counts[i])

            # Flow = the operators that CHANGE within the word
            # Count transitions between different fuses
            transitions = 0
            for i in range(1, len(word_glyphs)):
                if word_glyphs[i].fuse != word_glyphs[i-1].fuse:
                    transitions += 1

            # Word's structure_op = most common glyph structure_op
            s_counts = [0] * NUM_OPS
            for g in word_glyphs:
                s_counts[g.structure_op] += 1
            word_struct = max(range(NUM_OPS), key=lambda i: s_counts[i])

            # Word's flow_op = most common glyph flow_op
            f_counts = [0] * NUM_OPS
            for g in word_glyphs:
                f_counts[g.flow_op] += 1
            word_flow = max(range(NUM_OPS), key=lambda i: f_counts[i])

            # Word fuse: histogram majority of glyph fuses (NOT running CL).
            # Running CL always converges to HARMONY (absorber).
            # Histogram preserves the actual content operator.
            word_fuse = self._level_fuse([g.fuse for g in word_glyphs])

            # I/O balance of word
            avg_io = sum(g.io_ratio for g in word_glyphs) / len(word_glyphs)

            # Is this word a boundary? High transition rate = turbulent = boundary
            is_boundary = transitions > len(word_glyphs) * 0.6

            word_units.append(FractalUnit(
                level=3, structure_op=word_struct, flow_op=word_flow,
                fuse=word_fuse, io_ratio=avg_io,
                raw=w, is_boundary=is_boundary))

        return word_units

    # ── Level 5: Word Relations ──

    def _level_5_word_relations(self, words: List[FractalUnit]) -> List[FractalUnit]:
        """Relationships between adjacent words."""
        if len(words) < 2:
            return []

        rels = []
        for i in range(len(words) - 1):
            a = words[i]
            b = words[i + 1]

            # Relationship: which word's operator "wins"?
            # Use the word with stronger I/O imbalance (more definitive)
            if abs(a.io_ratio - 0.5) >= abs(b.io_ratio - 0.5):
                struct_op = a.fuse  # More definitive word leads
            else:
                struct_op = b.fuse

            # Flow = how their I/O balances differ
            io_diff = abs(a.io_ratio - b.io_ratio)
            if io_diff < 0.1:
                flow_op = HARMONY  # Similar balance = harmonious flow
            elif a.io_ratio > b.io_ratio:
                flow_op = COLLAPSE  # Structure decreasing = collapsing
            else:
                flow_op = PROGRESS  # Structure increasing = progressing

            # Fuse: the dominant of structure and flow in the pair
            if abs(a.io_ratio - 0.5) >= abs(b.io_ratio - 0.5):
                fuse = a.fuse
            else:
                fuse = b.fuse

            # Phrase boundary: different fuses = new phrase
            is_boundary = (a.fuse != b.fuse)

            avg_io = (a.io_ratio + b.io_ratio) / 2

            rels.append(FractalUnit(
                level=5, structure_op=struct_op, flow_op=flow_op,
                fuse=fuse, io_ratio=avg_io,
                raw=a.raw + ' ' + b.raw, is_boundary=is_boundary))

        return rels

    # ── Level 6: Triadic Becomings ──

    def _level_6_triadic_becomings(self, words: List[FractalUnit]) -> List[FractalUnit]:
        """Find being->doing->becoming progressions in word triplets."""
        if len(words) < 3:
            return []

        triads = []
        for i in range(len(words) - 2):
            w1 = words[i]
            w2 = words[i + 1]
            w3 = words[i + 2]

            # Check if fuses follow Being->Doing->Becoming
            is_triad = (
                w1.fuse in _BEING_OPS and
                w2.fuse in _DOING_OPS and
                w3.fuse in _BECOMING_OPS
            )

            if not is_triad:
                # Also check softer version: any BDC progression
                # Being = structure-dominant (high io_ratio)
                # Doing = balanced
                # Becoming = flow-dominant (low io_ratio)
                is_triad = (
                    w1.io_ratio > 0.52 and
                    abs(w2.io_ratio - 0.50) < 0.06 and
                    w3.io_ratio < 0.48
                )

            if is_triad:
                # The triad's identity = the becoming word's operator
                # (the RESULT of the being->doing->becoming progression)
                triads.append(FractalUnit(
                    level=6,
                    structure_op=w1.fuse,   # Being = structure
                    flow_op=w3.fuse,        # Becoming = flow
                    fuse=w3.fuse,           # Identity = what it becomes
                    io_ratio=(w1.io_ratio + w2.io_ratio + w3.io_ratio) / 3,
                    raw=w1.raw + ' ' + w2.raw + ' ' + w3.raw,
                    is_boundary=False))

        return triads

    # ── Level 7+: Recursive Grouping ──

    def _recursive_group(self, units: List[FractalUnit], level: int) -> List[FractalUnit]:
        """Group units into higher-level structures.

        Strategy: find consecutive same-fuse runs (structure zones)
        and transition points (flow zones). Each group becomes a new unit.
        """
        if len(units) < 2:
            return []

        groups = []
        current_group = [units[0]]

        for i in range(1, len(units)):
            if units[i].fuse == current_group[-1].fuse:
                # Same fuse: extend structure zone
                current_group.append(units[i])
            else:
                # Fuse changed: close current group, start new
                if len(current_group) >= 1:
                    groups.append(self._make_group(current_group, level))
                current_group = [units[i]]

        # Close last group
        if current_group:
            groups.append(self._make_group(current_group, level))

        return groups if len(groups) < len(units) else []  # Stop if no compression

    def _make_group(self, units: List[FractalUnit], level: int) -> FractalUnit:
        """Compose a group of units into a single higher-level unit."""
        if len(units) == 1:
            u = units[0]
            return FractalUnit(
                level=level, structure_op=u.structure_op, flow_op=u.flow_op,
                fuse=u.fuse, io_ratio=u.io_ratio, raw=u.raw,
                is_boundary=u.is_boundary)

        # Structure: the shared fuse (what the group IS)
        struct_op = units[0].fuse

        # Flow: CL composition across the group (how it evolves)
        running = units[0].fuse
        for u in units[1:]:
            running = CL[running][u.fuse]
        flow_op = running

        fuse = CL[struct_op][flow_op]
        avg_io = sum(u.io_ratio for u in units) / len(units)
        raw = ' '.join(u.raw for u in units)

        # Boundary if any sub-unit was a boundary
        is_boundary = any(u.is_boundary for u in units)

        return FractalUnit(
            level=level, structure_op=struct_op, flow_op=flow_op,
            fuse=fuse, io_ratio=avg_io, raw=raw,
            is_boundary=is_boundary)

    # ── Helper: classify force subspace ──

    def _classify_force_subspace(self, force_or_delta: tuple, subspace: str) -> int:
        """Classify a 5D vector into an operator for a specific subspace."""
        if subspace == 'structure':
            # Aperture (dim 0) vs Pressure (dim 1)
            a = abs(force_or_delta[0])
            p = abs(force_or_delta[1])
            if a >= p:
                return CHAOS if force_or_delta[0] >= 0 else LATTICE
            else:
                return COLLAPSE if force_or_delta[1] >= 0 else VOID
        else:  # 'flow'
            b = abs(force_or_delta[3])
            c = abs(force_or_delta[4])
            if b >= c:
                return HARMONY if force_or_delta[3] >= 0 else COUNTER
            else:
                return BALANCE if force_or_delta[4] >= 0 else BREATH

    # ── Helper: level fuse (histogram-based) ──

    def _level_fuse(self, ops: list) -> int:
        """Find the dominant operator in a sequence.

        Uses histogram majority, NOT running CL composition.
        Running CL always converges to HARMONY (absorber) and
        destroys content information. Histogram preserves it.

        If HARMONY is the only operator, return HARMONY.
        Otherwise return the most frequent NON-HARMONY operator,
        because HARMONY means 'well-formed' not 'content'.
        """
        if not ops:
            return VOID
        counts = [0] * NUM_OPS
        for op in ops:
            if 0 <= op < NUM_OPS:
                counts[op] += 1

        # Find most frequent non-HARMONY operator (content signal)
        best_op = VOID
        best_count = 0
        for i in range(NUM_OPS):
            if i == HARMONY:
                continue
            if counts[i] > best_count:
                best_count = counts[i]
                best_op = i

        # If no non-HARMONY operators exist, return HARMONY
        if best_count == 0:
            return HARMONY

        return best_op

    def _running_fuse(self, ops: list) -> int:
        """CL-compose a sequence of operators into a single fuse.
        Used for INTERACTION measurement (word relations), not identity."""
        if not ops:
            return VOID
        fuse = ops[0]
        for op in ops[1:]:
            fuse = CL[fuse][op]
        return fuse

    # ── Diagnostics ──

    def describe(self, result: ComprehensionResult) -> str:
        """Human-readable description of comprehension."""
        lines = []
        lines.append(f"Fractal comprehension: {result.depth} levels")
        lines.append(f"  Dominant: {OP_NAMES[result.dominant_op]}")
        lines.append(f"  I/O balance: {result.structure_flow_balance:.3f}")
        lines.append(f"  Boundaries: {result.boundaries} | "
                     f"Becomings: {result.becomings}")

        for i, fuse in enumerate(result.level_fuses):
            level_names = ['Glyph', 'Pairs', 'Curvature', 'Words',
                          'Word-Rels', 'Triads']
            name = level_names[i] if i < len(level_names) else f'L{i+6}'
            n_units = len(result.levels[i]) if i < len(result.levels) else 0
            lines.append(f"  L{i}: {name:10s} -> {OP_NAMES[fuse]:8s} "
                        f"({n_units} units)")

        if result.word_fuses:
            wf_names = [OP_NAMES[f][:3] for f in result.word_fuses[:12]]
            lines.append(f"  Word fuses: {' '.join(wf_names)}")

        return '\n'.join(lines)
