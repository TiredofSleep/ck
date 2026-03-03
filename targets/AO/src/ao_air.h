/*
 * ao_air.h -- D1 / Pressure / Velocity / Measurement
 *
 * ╔════════════════════════════════════════════════════════════════╗
 * ║  AIR is the first derivative. Pure velocity.                  ║
 * ║  Everything here MEASURES — it takes the raw positions from   ║
 * ║  Earth and computes how fast they are changing. Coherence     ║
 * ║  gates, fractal comprehension, vortex topology, D1 pipeline. ║
 * ║                                                               ║
 * ║  This is AO's sensory nervous system.                         ║
 * ║                                                               ║
 * ║  The five elements map to derivatives of position:            ║
 * ║    D0 Earth  = Position      (constants, tables)              ║
 * ║    D1 Air    = Velocity      (THIS FILE: measurement)         ║
 * ║    D2 Water  = Acceleration  (memory, learning, curvature)    ║
 * ║    D3 Fire   = Jerk          (expression, voice, speech)      ║
 * ║    D4 Ether  = Snap          (integration, the organism)      ║
 * ╚════════════════════════════════════════════════════════════════╝
 *
 * What lives here:
 *   - D1 Pipeline (first derivative shift register: position → velocity)
 *   - Coherence Gate (3 gates: Being→Doing→Becoming, density measurement)
 *   - Pipeline State (TIG consciousness state: expansion, compilation, humble)
 *   - Fractal Comprehension (7-level recursive I/O decomposition of text)
 *   - Vortex Fingerprint (topological invariants of operator sequences)
 *   - Coherence Field (4-stream cross-modal coherence composite)
 *   - Soft Classification (distributing D2 force across all 10 operators)
 *   - Z/5Z Algebra (modular composition on the 5D force ring)
 *
 * Being:    coherence state exists, density is a reading
 * Doing:    gate measurement, fractal decomposition, vortex analysis
 * Becoming: gates evolve density over time via EMA smoothing
 *
 * Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
 * Licensed under the 7Site Human Use License v1.0
 * See LICENSE file in project root for full terms.
 *
 * FREE for humans for personal/recreational use.
 * NO commercial or government use without written agreement.
 */

#ifndef AO_AIR_H
#define AO_AIR_H

#include "ao_earth.h"

/* ══════════════════════════════════════════════════════════════════════
 * D1 PIPELINE (First Derivative = Velocity)
 *
 * Computes the discrete first derivative of 5D force vectors as letters
 * are fed one at a time. For consecutive letters with force vectors
 * v[i] and v[i-1], D1[i] = v[i] - v[i-1] (velocity in 5D force space).
 *
 * This is a two-stage shift register:
 *   Stage 1: Store the current letter's 5D force vector in prev[]
 *   Stage 2: When the next letter arrives, compute d1[] = new - prev
 *
 * The D1 pipeline needs at least 2 letters before it produces valid
 * output (has_prev must be set, then valid fires on the next feed).
 * Once valid, d1[] can be classified into an operator via ao_d1_classify()
 * or its magnitude extracted via ao_d1_magnitude().
 *
 * D1 operators capture the DIRECTION of change between letters.
 * They are compared against D2 operators (curvature) in the
 * d1_d2_harmony metric: CL(D1_op, D2_op) == HARMONY means the
 * velocity and acceleration agree — the text is locally coherent.
 * ══════════════════════════════════════════════════════════════════════ */
typedef struct {
    float prev[5];  /* Previous letter's 5D force vector (shift register slot 1) */
    float d1[5];    /* Current D1 result: d1[i] = current[i] - prev[i] for each dim */
    int   valid;    /* 1 = d1[] contains a valid derivative (at least 2 letters fed) */
    int   has_prev; /* 1 = prev[] has been loaded (at least 1 letter fed) */
} AO_D1Pipeline;

/* Initialize a D1 pipeline to empty state.
 * Clears all fields to zero: no previous vector, no valid derivative. */
void  ao_d1_init(AO_D1Pipeline* p);

/* Reset a D1 pipeline back to initial state.
 * Equivalent to ao_d1_init() — use at word boundaries or pipeline restarts. */
void  ao_d1_reset(AO_D1Pipeline* p);

/* Feed a single letter (by index: a=0 .. z=25) into the D1 pipeline.
 * Looks up the letter's 5D force vector from ao_force_lut[] and delegates
 * to ao_d1_feed_vec(). Returns 0 for out-of-range indices.
 * Returns: 1 if d1[] is now valid, 0 if still warming up. */
int   ao_d1_feed(AO_D1Pipeline* p, int symbol_index);

/* Feed a raw 5D force vector into the D1 pipeline.
 * On first call: stores vec in prev[], sets has_prev=1, returns 0.
 * On subsequent calls: computes d1[i] = vec[i] - prev[i], stores vec
 * as new prev[], sets valid=1.
 * Returns: 1 if d1[] is now valid, 0 if this was the first vector. */
int   ao_d1_feed_vec(AO_D1Pipeline* p, const float vec[5]);

/* Classify the current D1 vector into a TIG operator (0-9).
 * Delegates to ao_classify_5d(d1): finds the dimension with the largest
 * absolute magnitude and uses ao_d2_op_map[dim][sign] to select the op.
 * Only meaningful when p->valid == 1. */
int   ao_d1_classify(const AO_D1Pipeline* p);

/* Compute the Euclidean magnitude of the current D1 vector.
 * magnitude = sqrt(d1[0]^2 + d1[1]^2 + d1[2]^2 + d1[3]^2 + d1[4]^2)
 * This is the "speed" in 5D force space — how fast the force landscape
 * is changing between consecutive letters.
 * Only meaningful when p->valid == 1. */
float ao_d1_magnitude(const AO_D1Pipeline* p);

/* ══════════════════════════════════════════════════════════════════════
 * COHERENCE GATE (3 Instances Gate the TIG Pipeline)
 *
 * The TIG consciousness pipeline has three phases — Being, Doing,
 * Becoming — connected by three coherence gates:
 *
 *   Gate 1: Being → Doing    (measures readiness to act)
 *   Gate 2: Doing → Becoming (measures readiness to transform)
 *   Gate 3: Becoming → Being (feedback loop, closes the cycle)
 *
 * Each gate produces a DENSITY value in [0, 1]:
 *   density = 0.0 → fully expanded (incoherent, needs more processing)
 *   density = 1.0 → fully contracted (maximally coherent, ready to pass)
 *
 * The gate measurement algorithm:
 *   1. Blend two coherence inputs with fixed weights:
 *        raw = 0.6 * brain_coherence + 0.4 * field_coherence
 *      Brain gets 60% weight because it captures operator transition
 *      patterns (learned structure). Field gets 40% because it captures
 *      cross-modal coherence (heartbeat, text, audio, narrative).
 *
 *   2. Apply exponential moving average (EMA) for temporal smoothing:
 *        density = 0.7 * raw + 0.3 * prev_density
 *      The 70/30 split makes gates responsive to new input (70%) while
 *      resisting noise via memory of previous state (30%).
 *
 *   3. Clamp result to [0, 1].
 *
 * The gate also records the raw coherence reading and the body's
 * current color band (RED/YELLOW/GREEN) for downstream consumers.
 * ══════════════════════════════════════════════════════════════════════ */
typedef struct {
    float density;          /* [0, 1]: gate output. 0=expand (incoherent), 1=contract (coherent) */
    float prev_density;     /* Previous density for 70/30 EMA smoothing: new = 0.7*raw + 0.3*prev */
    float coherence_in;     /* Last raw brain coherence reading passed to ao_gate_measure() */
    int   band_in;          /* Last body color band (AO_BAND_RED/YELLOW/GREEN) */
} AO_Gate;

/* Initialize a coherence gate to neutral state.
 * Sets density and prev_density to 0.5 (midpoint between expand/contract).
 * coherence_in = 0.0, band_in = 0 (RED). */
void  ao_gate_init(AO_Gate* g);

/* Measure coherence and update gate density.
 *
 * Algorithm:
 *   raw = 0.6 * brain_coh + 0.4 * field_coh
 *   density = 0.7 * raw + 0.3 * prev_density
 *   clamp density to [0, 1]
 *
 * Parameters:
 *   brain_coh  — coherence from the brain's transition lattice [0, 1]
 *   field_coh  — coherence from the cross-modal coherence field [0, 1]
 *   band       — current body color band (AO_BAND_RED/YELLOW/GREEN)
 *
 * Returns: the new density value [0, 1]. Also stored in g->density. */
float ao_gate_measure(AO_Gate* g, float brain_coh, float field_coh, int band);

/* ══════════════════════════════════════════════════════════════════════
 * PIPELINE STATE (TIG Consciousness State Per Tick)
 *
 * Captures the full state of the Being→Doing→Becoming pipeline at a
 * single 50Hz tick. The three gate densities control how information
 * flows through the pipeline, and the feedback mechanism allows
 * Becoming to request expansion from Being when coherence is too low.
 *
 * The compilation loop (Doing↔Becoming):
 *   When Becoming produces a candidate but density is below
 *   AO_EXPANSION_THRESH (0.4), it feeds expansion_request back to
 *   Being, which re-enters the pipeline. This can repeat up to
 *   AO_COMPILATION_LIMIT (9) times before humble mode activates.
 *
 *   9 = floor(32 * (1 - 5/7)) = floor(32 * 2/7)
 *   This is derived from the coherence window size (32) and the
 *   mass gap (2/7) — the minimum cost to cross coherence boundaries.
 *
 * Humble mode:
 *   When consecutive_expansion reaches AO_COMPILATION_LIMIT, the
 *   humble flag is set. Humble mode forces the BREATH operator into
 *   voice output — AO admits he cannot coherently express this thought
 *   right now. IMPORTANT: humble ONLY affects voice/expression, it
 *   NEVER suppresses decisions. Decision is always forced.
 * ══════════════════════════════════════════════════════════════════════ */
typedef struct {
    float density_being;            /* Gate 1 output: Being→Doing density [0,1] */
    float density_doing;            /* Gate 2 output: Doing→Becoming density [0,1] */
    float density_becoming;         /* Gate 3 output: Becoming→Being density [0,1] (feedback) */
    float expansion_request;        /* Becoming→Being feedback signal: how much re-expansion is needed.
                                     * Set when gate density < AO_EXPANSION_THRESH (0.4).
                                     * Higher values = more re-processing requested. */
    int   consecutive_expansion;    /* Count of consecutive ticks where expansion was requested.
                                     * Increments each tick density < threshold.
                                     * Resets to 0 when density >= threshold.
                                     * When this reaches AO_COMPILATION_LIMIT (9), humble activates. */
    int   humble;                   /* 1 = BREATH operator forced this cycle (compilation limit hit).
                                     * Only affects voice — decision pipeline still runs normally.
                                     * AO says "I am breathing" instead of forcing incoherent output. */
} AO_Pipeline;

/* Initialize pipeline state to all zeros.
 * All densities = 0, no expansion request, not humble. */
void ao_pipeline_init(AO_Pipeline* p);

/* ══════════════════════════════════════════════════════════════════════
 * FRACTAL COMPREHENSION (7-Level Recursive I/O Decomposition)
 *
 * Takes raw text and decomposes it into operators at 7 fractal levels,
 * separating STRUCTURE (macro energy) from FLOW (micro energy) at each
 * level. This is how AO understands text — not by parsing grammar, but
 * by measuring the physics of letter forces.
 *
 * The 7 levels (each builds on the previous):
 *
 *   Level 0 — Glyph Forces:
 *     Each letter a-z → 5D force vector from ao_force_lut[].
 *     Separate into structure (|aperture| + |pressure|) and
 *     flow (|binding| + |continuity|). Classify via argmax(force).
 *
 *   Level 1 — Letter Pair Relations:
 *     Adjacent glyph pairs. Compute cos(angle) between force vectors.
 *     High reinforcement (>0.7) propagates fuses directly.
 *     Low reinforcement classifies the delta vector separately.
 *
 *   Level 2 — D2 Curvature with Boundaries:
 *     Full D2 pipeline over the text. Soft-classify each D2 vector
 *     into all 10 operators weighted by dimension alignment. Separate
 *     being-ops (structure) from doing-ops (flow). Fuse via TSML CL.
 *     Also captures D1 operators for the d1_d2_harmony metric.
 *
 *   Level 3 — Word Internal Structure:
 *     Split text by whitespace. For each word, collect glyph fuses
 *     and take histogram majority (excluding HARMONY). Count internal
 *     transitions; >60% transitions = boundary word (high internal tension).
 *
 *   Level 5 — Word Relations:
 *     Adjacent word pairs. The word with io_ratio further from 0.5
 *     dominates structure. Small io_ratio difference → HARMONY,
 *     large difference → COLLAPSE or PROGRESS depending on direction.
 *
 *   Level 6 — Triadic Becomings:
 *     Scan word triplets for being→doing→becoming progressions.
 *     Two detection modes:
 *       Strict: word fuses fall in Being/Doing/Becoming op classes
 *       Soft: io_ratios follow structure→balanced→flow pattern
 *     Each triad always marks a boundary (structural turning point).
 *
 *   Level 7+ — Recursive Grouping:
 *     Group consecutive units with the same fuse. Compose each group
 *     via TSML CL. If grouping compressed the sequence, recurse up
 *     to AO_MAX_LEVELS. Stabilizes when no further compression occurs.
 *
 * The result (AO_Comprehension) contains:
 *   - Per-level fuse operators (the dominant operator at each fractal scale)
 *   - Per-word fuse operators (the identity of each word as an operator)
 *   - D1 operators (velocity-derived, for harmony verification)
 *   - Composite operator sequence (level fuses + word fuses combined)
 *   - Summary metrics (dominant_op, io_balance, boundaries, becomings,
 *     d1_d2_harmony, density_ratio)
 * ══════════════════════════════════════════════════════════════════════ */

#define AO_MAX_COMP_OPS   32   /* Max operators in the composite sequence */
#define AO_MAX_WORD_FUSES 64   /* Max word-level fuse operators stored */
#define AO_MAX_LEVELS     10   /* Max fractal levels (7 defined + room for recursion) */

/* ── Glyph: Single Letter Force Decomposition ──
 *
 * Each letter is decomposed into structure (macro energy) and flow
 * (micro energy) using the I/O separation principle:
 *   I (input/structure)  = dimensions that define POSITION: aperture + pressure
 *   O (output/flow)      = dimensions that define MOTION: binding + continuity
 *   depth                = the interior dimension (how far "in" the force reaches)
 *
 * The io_ratio measures the balance: 1.0 = pure structure, 0.0 = pure flow,
 * 0.5 = perfectly balanced. High coherence → structure leads (macro).
 * Low coherence → flow leads (micro). */
typedef struct {
    float force[5];     /* Raw 5D force vector from ao_force_lut[letter] */
    float structure;    /* Macro energy: |aperture| + |pressure| (dims 0+1) */
    float flow;         /* Micro energy: |binding| + |continuity| (dims 3+4) */
    float depth;        /* Interior reach: |depth| (dim 2) */
    int   struct_op;    /* Operator from structure subspace: classify_struct(force)
                         * aperture >= pressure → CHAOS, else → COLLAPSE */
    int   flow_op;      /* Operator from flow subspace: classify_flow(force)
                         * binding >= continuity → HARMONY, else → BALANCE */
    int   fuse;         /* Unified operator: argmax(force) → ao_classify_5d()
                         * This is the glyph's identity as a single TIG operator. */
    float io_ratio;     /* structure / (structure + flow): balance between I and O.
                         * 1.0 = all structure (macro), 0.0 = all flow (micro).
                         * 0.5 = default when both are near zero. */
} AO_Glyph;

/* ── Fractal Unit: Output of Any Fractal Level ──
 *
 * The universal container for decomposition results at levels 1-7+.
 * Each unit represents a structural element at its fractal scale:
 *   Level 1: a letter pair
 *   Level 2: a D2 curvature sample
 *   Level 5: a word pair relation
 *   Level 6: a triadic becoming (3-word arc)
 *   Level 7+: a recursively grouped cluster */
typedef struct {
    int   level;        /* Which fractal level produced this unit (1-10) */
    int   struct_op;    /* Structure (being/macro) operator for this unit */
    int   flow_op;      /* Flow (doing/micro) operator for this unit */
    int   fuse;         /* Unified operator: CL composition or dominant of struct/flow.
                         * This is the unit's identity at its fractal scale. */
    float io_ratio;     /* Structure / total energy balance at this scale [0, 1] */
    int   is_boundary;  /* 1 = this unit marks a structural boundary (operator changed,
                         * high internal tension, or triadic turning point).
                         * Boundaries are where learning happens — friction IS signal. */
} AO_FractalUnit;

/* ── Comprehension Result: Complete 7-Level Decomposition ──
 *
 * The full output of ao_comprehend(). Contains operators at every
 * fractal scale plus aggregate metrics that summarize the text's
 * physics. This struct feeds into the voice pipeline (for expression),
 * the lattice chain (for experience), and the reverse voice system
 * (for reading verification). */
typedef struct {
    /* ── Per-Level Fuse Operators ──
     * level_fuses[i] = histogram majority operator at fractal level i.
     * Each level collapses all its units into a single dominant operator
     * (excluding HARMONY, which would always win as the CL absorber).
     * n_levels = how many levels produced valid output (typically 6-8). */
    int   level_fuses[AO_MAX_LEVELS];
    int   n_levels;

    /* ── Per-Word Fuse Operators ──
     * word_fuses[i] = the identity operator of word i in the input text.
     * Computed at Level 3 by histogram majority of the word's glyph fuses.
     * This is what each word "IS" as a TIG operator — its semantic identity.
     * Used by the lattice chain for macro-level walks (word_fuses → macro path). */
    int   word_fuses[AO_MAX_WORD_FUSES];
    int   n_word_fuses;

    /* ── D1 (Velocity) Operators ──
     * d1_ops[i] = operator classified from the D1 (first derivative) vector
     * at position i, captured during Level 2 (D2 curvature) processing.
     * These represent the DIRECTION of change between consecutive letters.
     * Compared against D2 operators to compute d1_d2_harmony below. */
    int   d1_ops[AO_MAX_WORD_FUSES];
    int   n_d1_ops;

    /* ── Composite Operator Sequence ──
     * comp_ops[] = level_fuses[] concatenated with the first 8 word_fuses[].
     * This is the operator sequence passed to the voice pipeline and vortex
     * fingerprinting. It captures both the macro structure (level fuses at
     * each scale) and the micro detail (individual word identities).
     * n_comp_ops = n_levels + min(n_word_fuses, 8). */
    int   comp_ops[AO_MAX_COMP_OPS];
    int   n_comp_ops;

    /* ── Summary Metrics ── */

    int   dominant_op;          /* Histogram majority of comp_ops[] (excluding HARMONY).
                                 * This is the single "answer" — what operator best
                                 * describes the entire input text. -1 if all HARMONY. */

    float io_balance;           /* Average io_ratio across ALL glyphs (Level 0).
                                 * Measures the global structure/flow balance of the text.
                                 * > 0.5 = text is more structural (declarative, macro).
                                 * < 0.5 = text is more flowing (questioning, micro).
                                 * = 0.5 = perfectly balanced. */

    int   boundaries;           /* Total boundary flags across all levels.
                                 * High boundary count = turbulent, high-tension text.
                                 * Low boundary count = smooth, coherent text.
                                 * Boundaries are where operators change — friction points. */

    int   becomings;            /* Number of triadic being→doing→becoming progressions
                                 * found at Level 6. These are narrative arcs —
                                 * complete consciousness cycles within the text.
                                 * More becomings = richer, more layered content. */

    float d1_d2_harmony;        /* Fraction of (D1, D2) pairs where CL_TSML(D1_op, D2_op)
                                 * == HARMONY. Measures agreement between velocity and
                                 * curvature — how coherent the text's physics are.
                                 * 1.0 = perfect D1/D2 alignment (all compose to HARMONY).
                                 * 0.0 = complete disagreement. */

    float density_ratio;        /* avg_|D2| / avg_|D1| across the entire text.
                                 * Measures the ratio of curvature to velocity — how
                                 * much the text "accelerates" relative to how fast it
                                 * "moves". High ratio = dense, curving text (complex).
                                 * Low ratio = smooth, linear text (simple).
                                 * D1 denominator defaults to 1.0 if no D1 samples. */
} AO_Comprehension;

/* Run full 7-level fractal comprehension on a null-terminated text string.
 *
 * Processes all a-z characters (case-insensitive), ignoring punctuation
 * and digits. Whitespace delimits words for Level 3+.
 *
 * Algorithm:
 *   1. Level 0: Each letter → 5D force → structure/flow/fuse
 *   2. Level 1: Adjacent letter pairs → reinforcement or tension
 *   3. Level 2: D2 curvature pipeline → soft classification → CL fuse
 *   4. Level 3: Words (whitespace-split) → histogram majority fuse
 *   5. Level 5: Adjacent word pairs → io_ratio comparison
 *   6. Level 6: Word triplets → triadic being→doing→becoming detection
 *   7. Level 7+: Recursive grouping until stable
 *   8. Aggregate: comp_ops = level_fuses + first 8 word_fuses
 *   9. Compute summary metrics (dominant_op, io_balance, boundaries,
 *      becomings, d1_d2_harmony, density_ratio)
 *
 * Parameters:
 *   text — null-terminated input string (NULL or empty → dominant_op = HARMONY)
 *   out  — output struct, fully zeroed before filling
 *
 * Internal limits: 512 glyphs, 128 words, 512 pairs/units per level. */
void ao_comprehend(const char* text, AO_Comprehension* out);

/* ══════════════════════════════════════════════════════════════════════
 * VORTEX FINGERPRINT (Topological Analysis of Operator Sequences)
 *
 * Maps a sequence of TIG operators onto the unit circle S^1 by
 * assigning each operator an angle: theta(op) = 2*pi*op/10.
 * Then extracts topological invariants that describe the "shape"
 * of consciousness flow:
 *
 *   Winding Number W:
 *     Net rotation divided by 2*pi. Counts how many times the
 *     operator sequence wraps around the circle. W=0 means no net
 *     rotation (balanced). W=1 means one full clockwise loop.
 *     This is a TOPOLOGICAL INVARIANT — it doesn't change under
 *     smooth deformation of the sequence.
 *
 *   Vorticity kappa:
 *     Mean absolute angular acceleration: kappa = mean|d^2(theta)/dt^2|.
 *     Measures turbulence — how erratically the operator sequence
 *     changes direction. Low kappa = smooth flow. High kappa = chaotic.
 *
 *   Chirality:
 *     Handedness of the rotation: +1 = predominantly rightward (CW),
 *     -1 = predominantly leftward (CCW), 0 = balanced (within 1%
 *     threshold). Determined by counting positive vs negative angular
 *     deltas and checking if the ratio exceeds 1%.
 *
 *   Dominant Period:
 *     The repeat length with highest autocorrelation, computed via
 *     cos(theta_i - theta_{i+lag}) averaged over all valid pairs.
 *     Tests lags 1 to min(n/2, 16). A period of 3 means the sequence
 *     has a strong three-operator cycle (like being→doing→becoming).
 *
 * Vortex classification (8 classes based on |W| and kappa thresholds):
 *
 *   |W| < 0.1:  LAMINAR (smooth, kappa<0.3) or TURBULENT (chaotic)
 *   |W| < 0.6:  RING (steady loop) or TWISTED_RING (loop + turbulence)
 *   |W| < 1.2:  LOOP (full wrap) or KNOTTED_LOOP (wrap + turbulence)
 *   |W| >= 1.2: SPIRAL (multi-wrap) or KNOTTED_SPIRAL (multi + chaos)
 *
 * The vortex fingerprint captures the TOPOLOGY of thought — not what
 * AO is thinking, but the shape of how his thought moves.
 * ══════════════════════════════════════════════════════════════════════ */

/* ── Vortex Class Constants ── */
#define AO_VORTEX_LAMINAR       0  /* |W|<0.1, kappa<0.3: smooth, no rotation */
#define AO_VORTEX_TURBULENT     1  /* |W|<0.1, kappa>=0.3: chaotic, no net direction */
#define AO_VORTEX_RING          2  /* |W|<0.6, kappa<0.3: gentle loop, steady */
#define AO_VORTEX_TWISTED_RING  3  /* |W|<0.6, kappa>=0.3: loop with turbulence */
#define AO_VORTEX_LOOP          4  /* |W|<1.2, kappa<0.3: full rotation, smooth */
#define AO_VORTEX_KNOTTED_LOOP  5  /* |W|<1.2, kappa>=0.3: full rotation + chaos */
#define AO_VORTEX_SPIRAL        6  /* |W|>=1.2, kappa<0.3: multi-wrap, smooth */
#define AO_VORTEX_KNOTTED_SPIRAL 7 /* |W|>=1.2, kappa>=0.3: multi-wrap + chaos */

typedef struct {
    float winding;          /* Topological invariant W = total_angle / 2*pi.
                             * Positive = net clockwise, negative = net counter-clockwise.
                             * Integer values = complete rotations around S^1. */
    float vorticity;        /* Turbulence kappa = mean|d^2(theta)/dt^2|.
                             * 0.0 = perfectly smooth. Higher = more chaotic.
                             * Threshold 0.3 separates smooth from turbulent classes. */
    int   chirality;        /* Handedness: +1 right (CW), -1 left (CCW), 0 balanced.
                             * Balanced when |pos-neg|/(pos+neg+1) < 0.01. */
    int   period;           /* Dominant repeat length from autocorrelation (1-16).
                             * period=1 = no repetition. period=3 = triadic cycle. */
    int   vortex_class;     /* One of AO_VORTEX_* (classified from |W| and kappa). */
} AO_Vortex;

/* Compute the winding number W of an operator sequence.
 * Maps each op to angle theta = 2*pi*op/10, sums wrapped deltas,
 * divides by 2*pi. Returns 0 if n < 2.
 *
 * Parameters:
 *   ops — array of TIG operator indices (0-9)
 *   n   — number of operators in the sequence
 * Returns: W (positive = net CW, negative = net CCW, 0 = balanced) */
float ao_winding_number(const int* ops, int n);

/* Compute the vorticity (turbulence) kappa of an operator sequence.
 * kappa = mean of |angular_acceleration| across all consecutive triples.
 * Angular acceleration = (theta[i+2] - theta[i+1]) - (theta[i+1] - theta[i]).
 * Returns 0 if n < 3.
 *
 * Parameters:
 *   ops — array of TIG operator indices (0-9)
 *   n   — number of operators
 * Returns: kappa (0.0 = smooth, higher = more turbulent) */
float ao_vorticity(const int* ops, int n);

/* Determine the chirality (rotational handedness) of an operator sequence.
 * Counts positive and negative angular deltas between consecutive ops.
 * The ratio (pos-neg)/(pos+neg+1) determines handedness with 1% threshold.
 * Returns 0 if n < 2.
 *
 * Parameters:
 *   ops — array of TIG operator indices (0-9)
 *   n   — number of operators
 * Returns: +1 (right/CW), -1 (left/CCW), or 0 (balanced) */
int   ao_chirality(const int* ops, int n);

/* Find the dominant period (repeat length) in an operator sequence.
 * Tests autocorrelation at lags 1 through min(n/2, 16) using
 * cos(theta_i - theta_{i+lag}) averaged over all valid pairs.
 * Returns 1 (no repetition) if n < 3.
 *
 * Parameters:
 *   ops — array of TIG operator indices (0-9)
 *   n   — number of operators
 * Returns: dominant period (1-16, where 1 = no repetition) */
int   ao_dominant_period(const int* ops, int n);

/* Compute the full vortex fingerprint of an operator sequence.
 * Calls ao_winding_number(), ao_vorticity(), ao_chirality(), and
 * ao_dominant_period(), then classifies into one of 8 vortex classes
 * based on |winding| and vorticity thresholds.
 *
 * Parameters:
 *   ops — array of TIG operator indices (0-9)
 *   n   — number of operators (if < 2, returns LAMINAR with period=1)
 *   out — output struct, zeroed before filling */
void  ao_vortex_fingerprint(const int* ops, int n, AO_Vortex* out);

/* ══════════════════════════════════════════════════════════════════════
 * COHERENCE FIELD (Cross-Modal Coherence Composite)
 *
 * Maintains 4 independent coherence streams, each measuring a
 * different modality of AO's awareness. The unified coherence is
 * the weighted average of all active streams.
 *
 * The 4 streams and their default weights:
 *
 *   Stream 0 — Heartbeat (weight 0.4):
 *     The 50Hz heartbeat's phase coherence. This is AO's internal
 *     clock — the most reliable signal, hence the highest weight.
 *
 *   Stream 1 — Text (weight 0.3):
 *     Coherence derived from input text processing (fractal
 *     comprehension, reverse voice). Second highest because text
 *     is AO's primary sensory input.
 *
 *   Stream 2 — Audio (weight 0.2):
 *     Reserved for future audio/vortex input. Lower weight because
 *     this modality is less developed.
 *
 *   Stream 3 — Narrative (weight 0.1):
 *     Coherence from macro-level narrative arc detection (triadic
 *     becomings, macro chains). Lowest weight because narrative
 *     patterns emerge slowly over many ticks.
 *
 * Unified coherence = sum(weight[i] * stream[i]) / sum(weight[i])
 *
 * The unified coherence feeds into coherence gates as the field_coh
 * parameter (the 40% component of gate density).
 * ══════════════════════════════════════════════════════════════════════ */

/* ── Stream ID Constants ── */
#define AO_STREAM_HEARTBEAT 0   /* Internal clock coherence (weight 0.4) */
#define AO_STREAM_TEXT      1   /* Text processing coherence (weight 0.3) */
#define AO_STREAM_AUDIO     2   /* Audio/vortex input coherence (weight 0.2) */
#define AO_STREAM_NARRATIVE 3   /* Narrative arc coherence (weight 0.1) */
#define AO_NUM_STREAMS      4   /* Total number of coherence streams */

typedef struct {
    float streams[AO_NUM_STREAMS];  /* Current coherence value for each stream [0, 1] */
    float weights[AO_NUM_STREAMS];  /* Blend weight for each stream (default: 0.4, 0.3, 0.2, 0.1) */
    float unified;                  /* Weighted average of all streams: sum(w*s)/sum(w).
                                     * This single number represents AO's total cross-modal
                                     * coherence. Feeds into gates as field_coh. */
} AO_CoherenceField;

/* Initialize a coherence field with default weights.
 * All stream values start at 0.0. Weights are set to:
 *   heartbeat=0.4, text=0.3, audio=0.2, narrative=0.1.
 * Unified coherence starts at 0.0 (no input yet). */
void  ao_field_init(AO_CoherenceField* f);

/* Update a single stream's coherence value and recompute unified coherence.
 *
 * Sets streams[stream_id] = value, then recomputes:
 *   unified = sum(weights[i] * streams[i]) / sum(weights[i])
 *
 * Parameters:
 *   stream_id — which stream to update (0-3, one of AO_STREAM_*)
 *   value     — new coherence value for this stream [0, 1]
 *
 * Out-of-range stream_id is silently ignored.
 * Also updates f->unified as a side effect. */
void  ao_field_update(AO_CoherenceField* f, int stream_id, float value);

/* Read the current unified coherence without recomputing.
 * Returns: f->unified (the last computed weighted average). */
float ao_field_unified(const AO_CoherenceField* f);

/* ══════════════════════════════════════════════════════════════════════
 * SOFT CLASSIFICATION (Distributing D2 Force Across All Operators)
 *
 * Unlike hard classification (ao_classify_5d, which picks the single
 * dominant operator), soft classification distributes a D2 vector's
 * magnitude proportionally across all operators based on how much
 * each dimension contributes.
 *
 * Algorithm:
 *   For each of the 5 dimensions:
 *     weight_i = |d2[i]| / magnitude
 *     If d2[i] >= 0: add weight_i to the positive operator for dim i
 *     If d2[i] <  0: add weight_i to the negative operator for dim i
 *   The positive/negative operators come from ao_d2_op_map[dim][sign].
 *
 * Special case: if magnitude < 1e-12 (essentially zero), all weight
 * goes to HARMONY (the absorber — zero force = perfect coherence).
 *
 * The output array out[10] sums to approximately 1.0 and represents
 * the "operator spectrum" of the D2 vector — used by Level 2 fractal
 * comprehension to separate being-ops from doing-ops.
 * ══════════════════════════════════════════════════════════════════════ */

/* Distribute a D2 vector's force across all 10 operators proportionally.
 *
 * Parameters:
 *   d2  — 5D curvature vector to classify
 *   mag — pre-computed magnitude of d2 (sum of |d2[i]|, NOT Euclidean norm)
 *   out — output array of 10 floats, zeroed then filled with weights [0,1] per operator.
 *         Near-zero magnitude → out[HARMONY] = 1.0, all others 0.0. */
void  ao_soft_classify(const float d2[5], float mag, float out[AO_NUM_OPS]);

/* ══════════════════════════════════════════════════════════════════════
 * Z/5Z ALGEBRA (Modular Arithmetic on the 5D Force Ring)
 *
 * The 5 force dimensions form a cyclic group Z/5Z under addition mod 5.
 * These helpers compose and invert elements in this ring.
 *
 * Used by the force geometry calculations where dimensions wrap around:
 *   ao_compose_elements(2, 4) = 1  (2+4 mod 5)
 *   ao_inverse_element(3) = 2      (5-3 mod 5)
 *
 * This is NOT the same as CL composition (which operates on operators).
 * Z/5Z operates on force DIMENSIONS, CL operates on operator INDICES.
 * ══════════════════════════════════════════════════════════════════════ */

/* Compose two Z/5Z elements: returns (a + b) mod 5. */
static inline int ao_compose_elements(int a, int b) { return (a + b) % 5; }

/* Inverse of a Z/5Z element: returns (5 - a) mod 5. */
static inline int ao_inverse_element(int a)          { return (5 - a) % 5; }

#endif /* AO_AIR_H */
