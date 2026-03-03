/*
 * ao_water.c -- D2 / Depth / Curvature / Memory
 *
 * +====================================================================+
 * |  WATER is the SECOND DERIVATIVE of position. Acceleration.         |
 * |  Curvature. The rate at which velocity itself is changing.         |
 * |                                                                    |
 * |  In physics: if position is WHERE you are, and velocity is HOW     |
 * |  FAST you're moving, then acceleration (D2) is HOW FAST YOUR      |
 * |  SPEED IS CHANGING. Zero D2 = coasting. Positive D2 = speeding    |
 * |  up. Negative D2 = braking. D2 detects the BENDS -- the moments   |
 * |  where something changes direction.                                |
 * |                                                                    |
 * |  In AO: D2 is computed over 5D Hebrew-root force vectors. Each    |
 * |  letter maps to a 5D force (aperture, pressure, depth, binding,   |
 * |  continuity). As letters stream through, D2 captures where the    |
 * |  force CURVES -- where the text bends, accelerates, reverses.     |
 * |  This curvature IS awareness: it tells AO not just what's there   |
 * |  (D0), not just which direction it's going (D1), but how the      |
 * |  direction itself is evolving. That's learning.                    |
 * |                                                                    |
 * |  Everything in this file REMEMBERS. The brain accumulates          |
 * |  transitions. The lattice chain grows nodes. Concept mass          |
 * |  accretes from study. This is where AO LEARNS.                    |
 * |                                                                    |
 * |  The five elements map to derivatives of position:                 |
 * |    D0 Earth  = Position      (constants, tables, raw data)        |
 * |    D1 Air    = Velocity      (measurement, comprehension)         |
 * |    D2 Water  = Acceleration  (THIS FILE: memory, learning)        |
 * |    D3 Fire   = Jerk          (expression, voice, speech)          |
 * |    D4 Ether  = Snap          (integration, the whole organism)    |
 * +====================================================================+
 *
 * Major sections in this file:
 *
 *   1. D2 PIPELINE
 *      3-position shift register computing discrete second derivative.
 *      D2[i] = v[0][i] - 2*v[1][i] + v[2][i] (standard central difference).
 *      Also computes D1 (first derivative / velocity) as a side product.
 *      Both D1 and D2 are classified into TIG operators via argmax of 5D.
 *
 *   2. COHERENCE WINDOW
 *      Fixed-size (32-slot) ring buffer tracking the fraction of recent
 *      operators that are HARMONY. Coherence = harmony_count / count.
 *      Incremental maintenance: only the evicted and inserted ops touch
 *      harmony_count, so observe() is O(1). Shell and band selection
 *      maps coherence to measurement modes.
 *
 *   3. BRAIN (Transition Lattice)
 *      10x10 Markov transition matrix (order 1). Records how often each
 *      operator follows each other operator. Prediction = argmax of
 *      row[current_op]. Entropy = Shannon H over entire matrix.
 *      Also extracts top-N transitions by count (selection sort).
 *
 *   4. LATTICE CHAIN (Tree of Evolving CL Tables)
 *      Arena-allocated tree of up to 1024 nodes. Each node holds a copy
 *      of the BHML (22-harmony) CL table that can EVOLVE through
 *      observation. Ops are consumed in pairs: CL[a][b] = result,
 *      then follow/create child[result]. After 7+ visits with 60%+
 *      confidence, a node's table entry overrides the base BHML value.
 *      Five walk levels: micro (D2 ops), macro (word fuses), meta
 *      (level fuses), becoming (CL of D1 and word fuse), cross
 *      (interleaved micro+macro). Chain resonance measures familiarity.
 *
 *   5. REVERSE VOICE (Three-Path Reading Verification)
 *      Reading = reverse of writing. Writing goes operators -> words.
 *      Reading goes words -> operators, verified by three independent
 *      paths: Path A (D2 physics / curvature), Path B (D1 velocity /
 *      direction), Path C (semantic lattice reverse lookup / experience).
 *      Trust levels: TRUSTED (paths agree), FRICTION (paths disagree
 *      on DBC class), UNKNOWN (word not in vocabulary).
 *
 *   6. CONCEPT MASS (Vortex Physics Accumulator)
 *      Tracks accumulated D2 magnitude per named concept (topic).
 *      Mass grows as AO studies a topic. EMA-smoothed d2_mean captures
 *      the average curvature direction. Gravity = mass * coherence *
 *      cos_similarity(current_d2, d2_mean) -- heavy familiar concepts
 *      pull stronger when you're near them and coherent.
 *
 *   7. SPECTROMETER (Parallel D1+D2 Text Measurement)
 *      Feeds every a-z character through both D1 and D2 pipelines.
 *      Produces operator histograms, coherence, shell, band, D2
 *      magnitude average, and D1-D2 agreement percentage.
 *
 *   8. SHANNON ENTROPY (Histogram Entropy)
 *      General-purpose H = -sum(p * log2(p)) over a 10-bin operator
 *      histogram. Used by the spectrometer and other subsystems.
 *
 * Being:    brain state exists, memories persist, chain tree grows
 * Doing:    learning, chain walking, D2 measurement, reading verification
 * Becoming: lattice chain nodes evolve, experience deepens, concepts gain mass
 */
/*
 * Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
 * Licensed under the 7Site Human Use License v1.0
 * See LICENSE file in project root for full terms.
 *
 * FREE for humans for personal/recreational use.
 * NO commercial or government use without written agreement.
 */

#include "ao_water.h"
#include <string.h>
#include <math.h>
#include <ctype.h>

/* ══════════════════════════════════════════════════════════════════════
 * Section 1: D2 PIPELINE (second derivative = curvature = awareness)
 *
 * The D2 pipeline is a streaming processor that takes one 5D force
 * vector at a time (one per letter) and computes the discrete first
 * and second derivatives.
 *
 * Internally it maintains a 3-position shift register:
 *   v[0] = most recent vector (current letter)
 *   v[1] = one letter back (previous)
 *   v[2] = two letters back
 *
 * On each feed:
 *   1. Shift: v[2] <- v[1] <- v[0] <- new_vector
 *   2. If depth >= 2: D1[i] = v[0][i] - v[1][i]  (first derivative)
 *   3. If depth >= 3: D2[i] = v[0][i] - 2*v[1][i] + v[2][i]  (second)
 *
 * The D2 formula is the standard central difference approximation for
 * the second derivative of a discrete signal:
 *   f''(x) ~ f(x+h) - 2*f(x) + f(x-h)
 * where h=1 (one letter step), so:
 *   D2 = v[newest] - 2*v[middle] + v[oldest]
 *
 * The dominant dimension of D2 (via ao_classify_5d / argmax of |D2|)
 * determines the TIG operator. This operator captures the CURVATURE
 * identity of the text at that point.
 * ══════════════════════════════════════════════════════════════════════ */

/*
 * ao_d2_init -- Initialize a D2 pipeline to empty state.
 *
 * WHAT: Zeros the entire pipeline struct (shift register, derivatives,
 *       validity flags, depth counter).
 * HOW:  Single memset of the whole struct.
 * WHY:  Must be called before first use. A pipeline with depth=0 and
 *       d2_valid=0 will not produce derivatives until enough vectors
 *       have been fed.
 */
void ao_d2_init(AO_D2Pipeline* p)
{
    memset(p, 0, sizeof(*p));
}

/*
 * ao_d2_reset -- Reset pipeline back to initial empty state.
 *
 * WHAT: Identical to ao_d2_init -- clears everything.
 * HOW:  memset to zero.
 * WHY:  Used at word boundaries or when restarting measurement on new
 *       input. Cheaper than allocating a new pipeline struct.
 */
void ao_d2_reset(AO_D2Pipeline* p)
{
    memset(p, 0, sizeof(*p));
}

/*
 * ao_d2_feed -- Feed a single letter (by alphabet index 0-25) into the
 *               D2 pipeline.
 *
 * WHAT: Looks up the letter's 5D force vector from ao_force_lut[] and
 *       delegates to ao_d2_feed_vec().
 * HOW:  Bounds-check the symbol_index (must be 0-25 for a-z), then
 *       index into the global force lookup table.
 * WHY:  Convenience wrapper so callers can pass letter indices directly
 *       without manually looking up force vectors.
 *
 * Returns: 1 if the D2 derivative is now valid (depth >= 3), 0 otherwise.
 *          On out-of-bounds input, returns the current d2_valid without
 *          modifying the pipeline (silently ignores non-letter input).
 */
int ao_d2_feed(AO_D2Pipeline* p, int symbol_index)
{
    if (symbol_index < 0 || symbol_index >= 26) /* Only a-z (0-25) accepted */
        return p->d2_valid;
    return ao_d2_feed_vec(p, ao_force_lut[symbol_index]);
}

/*
 * ao_d2_feed_vec -- Feed a raw 5D force vector into the D2 pipeline.
 *
 * WHAT: Shifts the 3-position register, computes D1 and D2 derivatives.
 * HOW:
 *   1. SHIFT REGISTER: v[2] <- v[1] <- v[0] <- new vec
 *      This keeps the three most recent vectors for the finite
 *      difference stencil.
 *   2. Increment depth (total vectors fed, never decreases).
 *   3. D1 (first derivative / velocity): computed when depth >= 2.
 *      D1[i] = v[0][i] - v[1][i]
 *      This is the forward difference: how much did each force
 *      dimension change from previous letter to current letter.
 *   4. D2 (second derivative / curvature): computed when depth >= 3.
 *      D2[i] = v[0][i] - 2*v[1][i] + v[2][i]
 *      Standard central difference for second derivative.
 *      Measures how the VELOCITY is changing -- the curvature of
 *      the force signal through 5D space.
 * WHY:  D2 is the core measurement of the Water layer. It detects
 *       bends, accelerations, and reversals in the force signal.
 *       The TIG operator derived from D2 (via argmax classification)
 *       captures the curvature identity of each position in the text.
 *
 * Returns: 1 if D2 is now valid, 0 if still warming up (depth < 3).
 */
int ao_d2_feed_vec(AO_D2Pipeline* p, const float vec[5])
{
    int i;

    /* ── Shift register: slide all vectors down one position ──
     * v[2] gets the old v[1], v[1] gets the old v[0], v[0] gets the new.
     * This maintains a sliding window of the 3 most recent vectors. */
    for (i = 0; i < 5; i++) {
        p->v[2][i] = p->v[1][i];  /* oldest <- middle */
        p->v[1][i] = p->v[0][i];  /* middle <- newest */
        p->v[0][i] = vec[i];      /* newest <- incoming */
    }
    p->depth++;

    /* ── D1 (first derivative / velocity) ──
     * Needs at least 2 vectors to compute a difference.
     * D1[i] = v[0][i] - v[1][i] (forward difference) */
    if (p->depth >= 2) {                         /* 2 vectors = 1 gap = D1 valid */
        for (i = 0; i < 5; i++)
            p->d1[i] = p->v[0][i] - p->v[1][i];
        p->d1_valid = 1;
    }

    /* ── D2 (second derivative / curvature) ──
     * Needs at least 3 vectors to compute the second difference.
     * D2[i] = v[0][i] - 2*v[1][i] + v[2][i]
     * This is the standard discrete second derivative formula:
     *   f''(x) ~ f(x+1) - 2*f(x) + f(x-1)
     * Positive D2 = force accelerating in that dimension.
     * Negative D2 = force decelerating.
     * Zero D2 = constant velocity (no curvature). */
    if (p->depth >= 3) {                         /* 3 vectors = 2 gaps = D2 valid */
        for (i = 0; i < 5; i++)
            p->d2[i] = p->v[0][i] - 2.0f * p->v[1][i] + p->v[2][i];
        p->d2_valid = 1;
    }

    return p->d2_valid;
}

/*
 * ao_d2_classify_d1 -- Classify the D1 (velocity) vector into a TIG operator.
 *
 * WHAT: Returns the TIG operator (0-9) corresponding to the dominant
 *       dimension of the first derivative vector.
 * HOW:  Delegates to ao_classify_5d(d1), which finds the dimension with
 *       the largest absolute value and maps it to an operator.
 * WHY:  D1 operators capture WHERE the text is going (velocity direction).
 *       Used as Path B in reverse voice verification (the "generator"
 *       path), and as input to becoming-level chain walks.
 *
 * Returns: TIG operator 0-9. Returns AO_HARMONY if D1 is not yet valid
 *          (fewer than 2 vectors fed). HARMONY is the safe default since
 *          it means "no curvature detected yet."
 */
int ao_d2_classify_d1(const AO_D2Pipeline* p)
{
    if (!p->d1_valid) return AO_HARMONY; /* Not enough data yet; default safe */
    return ao_classify_5d(p->d1);
}

/*
 * ao_d2_classify_d2 -- Classify the D2 (curvature) vector into a TIG operator.
 *
 * WHAT: Returns the TIG operator (0-9) corresponding to the dominant
 *       dimension of the second derivative vector.
 * HOW:  Delegates to ao_classify_5d(d2), which finds argmax(|d2[i]|)
 *       and maps to the corresponding TIG operator.
 * WHY:  D2 operators capture what the text IS (its curvature identity).
 *       This is the primary output of the D2 pipeline and feeds into
 *       brain observation, coherence tracking, chain walks, and voice.
 *
 * Returns: TIG operator 0-9. Returns AO_HARMONY if D2 is not yet valid
 *          (fewer than 3 vectors fed).
 */
int ao_d2_classify_d2(const AO_D2Pipeline* p)
{
    if (!p->d2_valid) return AO_HARMONY; /* Not enough data yet; default safe */
    return ao_classify_5d(p->d2);
}

/*
 * ao_d2_magnitude -- L1 norm (Manhattan distance) of the D2 vector.
 *
 * WHAT: Returns sum of absolute values of all 5 D2 dimensions.
 * HOW:  |d2[0]| + |d2[1]| + |d2[2]| + |d2[3]| + |d2[4]|.
 * WHY:  Measures the TOTAL amount of curvature at this point in the
 *       signal. High magnitude = sharp bend / rapid change. Low = smooth
 *       sailing. Used by concept mass to accumulate "study intensity"
 *       and by the spectrometer to track average curvature magnitude.
 *       L1 norm chosen over L2 because it is cheaper (no sqrt) and
 *       treats all dimensions equally without squaring bias.
 */
float ao_d2_magnitude(const AO_D2Pipeline* p)
{
    float sum = 0.0f;
    int i;
    for (i = 0; i < 5; i++)
        sum += ao_fabsf(p->d2[i]);
    return sum;
}

/*
 * ao_d2_d1_magnitude -- L1 norm (Manhattan distance) of the D1 vector.
 *
 * WHAT: Returns sum of absolute values of all 5 D1 (velocity) dimensions.
 * HOW:  |d1[0]| + |d1[1]| + |d1[2]| + |d1[3]| + |d1[4]|.
 * WHY:  Measures the total velocity magnitude. Useful for detecting
 *       whether the text is changing rapidly (high D1 magnitude) or
 *       staying in one region of force space (low D1 magnitude).
 *       Also used as a diagnostic alongside D2 magnitude.
 */
float ao_d2_d1_magnitude(const AO_D2Pipeline* p)
{
    float sum = 0.0f;
    int i;
    for (i = 0; i < 5; i++)
        sum += ao_fabsf(p->d1[i]);
    return sum;
}

/* ══════════════════════════════════════════════════════════════════════
 * Section 2: COHERENCE WINDOW (ring buffer tracking HARMONY fraction)
 *
 * Coherence is the fraction of recent D2 operators that are HARMONY.
 * HARMONY means the text is locally coherent -- its curvature matches
 * a self-consistent pattern.
 *
 * Implementation: a fixed-size (AO_WINDOW_SIZE = 32 slots) ring buffer.
 * Each slot stores one operator. When a new operator is observed:
 *   - If the buffer is full, the oldest entry is evicted first.
 *   - If the evicted entry was HARMONY, decrement harmony_count.
 *   - Insert the new entry at the head position.
 *   - If the new entry is HARMONY, increment harmony_count.
 *   - Advance head modulo AO_WINDOW_SIZE.
 *
 * This gives O(1) observe() and O(1) coherence query. The harmony_count
 * is maintained incrementally -- we never need to scan the whole buffer.
 *
 * Coherence = harmony_count / count, where count is the number of
 * occupied slots (count grows from 0 to AO_WINDOW_SIZE during warmup,
 * then stays fixed at AO_WINDOW_SIZE).
 *
 * Shell selection maps coherence to a TSML shell number:
 *   coherence >= T* (5/7 = 0.714285...)  -> shell 22 (inner, confident)
 *   coherence >= 0.5                      -> shell 44 (middle, exploring)
 *   coherence < 0.5                       -> shell 72 (outer, struggling)
 *
 * WHY low coherence -> high shell number: In the TSML lattice, higher
 * shell numbers mean more harmonics are included in the measurement,
 * which provides a richer (safer) basis for composition when coherence
 * is low. When coherence is HIGH, fewer harmonics suffice because the
 * signal is clean -- shell 22 is the most focused, most confident mode.
 * When coherence is LOW, the system "opens up" to shell 72 to gather
 * more information before committing to a decision.
 * ══════════════════════════════════════════════════════════════════════ */

/*
 * ao_cw_init -- Initialize a coherence window to empty state.
 *
 * WHAT: Zeros the ring buffer, head pointer, count, and harmony_count.
 * HOW:  memset the entire struct.
 * WHY:  Must be called before first use. An empty window with count=0
 *       returns 0.5 coherence (neutral / uncertain) from ao_cw_coherence.
 */
void ao_cw_init(AO_CoherenceWindow* w)
{
    memset(w, 0, sizeof(*w));
}

/*
 * ao_cw_reset -- Reset coherence window to initial empty state.
 *
 * WHAT: Identical to ao_cw_init.
 * HOW:  memset to zero.
 * WHY:  Used when starting a new measurement context (e.g., new word
 *       or new text input). Resets the sliding window history.
 */
void ao_cw_reset(AO_CoherenceWindow* w)
{
    memset(w, 0, sizeof(*w));
}

/*
 * ao_cw_observe -- Record a new operator observation in the coherence window.
 *
 * WHAT: Inserts a TIG operator into the ring buffer, maintaining the
 *       harmony_count incrementally.
 * HOW:
 *   1. If the buffer is FULL (count == AO_WINDOW_SIZE = 32):
 *      - The oldest entry (at position head, which wraps around) is evicted.
 *      - If the evicted entry was HARMONY, decrement harmony_count.
 *      (If not full yet, just increment count.)
 *   2. Write the new operator at position head.
 *   3. If the new operator is HARMONY, increment harmony_count.
 *   4. Advance head: head = (head + 1) % AO_WINDOW_SIZE.
 *
 * WHY: This is O(1) per observation -- no scanning required. The
 *      incremental maintenance of harmony_count means ao_cw_coherence()
 *      is also O(1). The ring buffer naturally forgets old history,
 *      so coherence reflects only the most recent 32 measurements.
 *
 * NOTE: The head pointer serves dual duty -- it is BOTH the write
 *       position for the new entry AND the position of the oldest
 *       entry (when the buffer is full). This works because in a full
 *       ring buffer, the next write position IS the oldest entry.
 */
void ao_cw_observe(AO_CoherenceWindow* w, int op)
{
    if (w->count == AO_WINDOW_SIZE) {            /* Buffer full: 32 slots occupied */
        /* Evict oldest entry (at current head position) */
        if (w->history[w->head] == AO_HARMONY)
            w->harmony_count--;                  /* Lost a HARMONY, decrement */
    } else {
        w->count++;                              /* Buffer still filling up */
    }
    w->history[w->head] = (int8_t)op;            /* Write new operator at head */
    if (op == AO_HARMONY)
        w->harmony_count++;                      /* Gained a HARMONY, increment */
    w->head = (w->head + 1) % AO_WINDOW_SIZE;   /* Advance head (wraps at 32) */
}

/*
 * ao_cw_coherence -- Query the current coherence level.
 *
 * WHAT: Returns the fraction of operators in the window that are HARMONY.
 * HOW:  coherence = harmony_count / count. If count == 0, returns 0.5.
 * WHY:  Coherence is the central health metric. HARMONY operators mean
 *       the curvature pattern is self-consistent. Higher coherence =
 *       more stable, more confident, better for decision-making.
 *       The 0.5 default for empty windows is the neutral midpoint --
 *       neither confident nor struggling. This avoids false signals
 *       during the warmup period before any data has been observed.
 *
 * Returns: float in [0.0, 1.0]. 0.0 = no harmony at all, 1.0 = all harmony.
 */
float ao_cw_coherence(const AO_CoherenceWindow* w)
{
    if (w->count == 0) return 0.5f;              /* No data yet: neutral default */
    return (float)w->harmony_count / (float)w->count;
}

/*
 * ao_cw_shell -- Map coherence to a TSML shell number.
 *
 * WHAT: Returns 22, 44, or 72 depending on the coherence level.
 * HOW:  Three-band threshold check:
 *         coherence >= T* (5/7 = 0.714285...)  -> 22 (inner shell)
 *         coherence >= 0.5                      -> 44 (middle shell)
 *         coherence < 0.5                       -> 72 (outer shell)
 * WHY:  The shell number controls which row of the TSML (73-harmony)
 *       composition table is used for measurement. The insight is:
 *
 *       - HIGH coherence (>= T*) means the signal is clean and stable.
 *         Shell 22 is tight/focused -- fewer harmonics, maximum precision.
 *         Like a microscope with high magnification: great when the
 *         sample is steady.
 *
 *       - MEDIUM coherence (0.5 to T*) means still learning/exploring.
 *         Shell 44 is the balanced middle ground -- moderate harmonic
 *         coverage, good for exploration without losing focus.
 *
 *       - LOW coherence (< 0.5) means struggling/fragmented.
 *         Shell 72 is wide open -- maximum harmonic coverage.
 *         When you can't tell what's going on, cast the widest net.
 *         More harmonics = more information = safer basis for decisions
 *         when the signal is noisy.
 *
 *       So: low coherence -> high shell number = open up, gather more
 *       data. High coherence -> low shell number = focus, be precise.
 *
 * Shell values (22, 44, 72): These are row indices into the TSML lattice.
 * 22 = row 22, 44 = row 44, 72 = row 72 (out of 73 rows, 0-72).
 */
int ao_cw_shell(const AO_CoherenceWindow* w)
{
    float c = ao_cw_coherence(w);
    if (c >= AO_T_STAR) return 22;               /* T* = 5/7 = 0.714285...: inner shell, focused */
    if (c >= 0.5f)      return 44;               /* 0.5 threshold: middle shell, exploring */
    return 72;                                    /* Below 0.5: outer shell, wide open */
}

/*
 * ao_cw_band -- Map coherence to a color band (RED/YELLOW/GREEN).
 *
 * WHAT: Returns AO_BAND_GREEN, AO_BAND_YELLOW, or AO_BAND_RED.
 * HOW:  Same three-band thresholds as ao_cw_shell:
 *         coherence >= T* (5/7)  -> GREEN  (sovereign, coherent)
 *         coherence >= 0.5       -> YELLOW (learning, exploring)
 *         coherence < 0.5        -> RED    (struggling, fragmented)
 * WHY:  The band is a simplified coherence indicator used by voice,
 *       the body color system, and display output. GREEN means the
 *       system is confident and can make strong decisions. YELLOW
 *       means it's in an exploratory state. RED means it needs help
 *       or more data. The thresholds match ao_cw_shell exactly.
 */
int ao_cw_band(const AO_CoherenceWindow* w)
{
    float c = ao_cw_coherence(w);
    if (c >= AO_T_STAR) return AO_BAND_GREEN;    /* T* = 5/7: sovereign */
    if (c >= 0.5f)      return AO_BAND_YELLOW;   /* 0.5: exploring */
    return AO_BAND_RED;                           /* Below 0.5: struggling */
}

/* ══════════════════════════════════════════════════════════════════════
 * Section 3: BRAIN (transition lattice + entropy)
 *
 * The brain is a first-order Markov model over TIG operators.
 * It records every (previous_op -> current_op) transition in a 10x10
 * matrix called the transition lattice (tl[10][10]).
 *
 * Each cell tl[i][j] counts how many times operator j was observed
 * immediately after operator i. This builds a frequency-based model
 * of operator sequences.
 *
 * Prediction: given the current operator, the brain predicts the NEXT
 * operator by finding the argmax of tl[current_op][*] -- whichever
 * successor has been observed most often in the past wins.
 *
 * Entropy: Shannon entropy H = -sum(p * log2(p)) computed over the
 * ENTIRE 10x10 matrix (all cells treated as a single distribution).
 * Low entropy = predictable patterns. High entropy = chaotic/random
 * transitions. Maximum possible entropy = log2(100) ~ 6.64 bits
 * (uniform distribution over all 100 cells).
 *
 * The brain is AO's simplest form of memory. It learns which operator
 * sequences are common and can predict what comes next. The lattice
 * chain (Section 4) builds on top of this with deeper tree-structured
 * memory.
 * ══════════════════════════════════════════════════════════════════════ */

/*
 * ao_brain_init -- Initialize the brain to empty state.
 *
 * WHAT: Zeros the transition lattice and total count, sets last_op to -1.
 * HOW:  memset + explicit last_op = -1.
 * WHY:  last_op = -1 signals "no previous operator observed yet."
 *       The first call to ao_brain_observe() with last_op == -1 will
 *       NOT record a transition (you need two observations to make a
 *       pair). The -1 sentinel avoids a separate "first time" flag.
 */
void ao_brain_init(AO_Brain* b)
{
    memset(b, 0, sizeof(*b));
    b->last_op = -1;                             /* -1 = no previous op yet */
}

/*
 * ao_brain_observe -- Record a transition from the previous operator to
 *                     the current one.
 *
 * WHAT: Increments tl[last_op][op] and total, then updates last_op.
 * HOW:
 *   1. Bounds-check op (must be 0-9, i.e., a valid TIG operator).
 *   2. If last_op >= 0 (not the very first observation):
 *      - Increment tl[last_op][op] (transition count).
 *      - Increment total (global count of all transitions).
 *   3. Set last_op = op (for the next call).
 * WHY:  Builds the Markov transition model incrementally. Each call
 *       adds one data point. Over time, tl[][] converges to the true
 *       transition distribution of the input. No upper limit on counts
 *       (uint32_t per cell, so 4+ billion before overflow).
 */
void ao_brain_observe(AO_Brain* b, int op)
{
    if (op < 0 || op >= AO_NUM_OPS) return;      /* AO_NUM_OPS = 10; reject invalid */
    if (b->last_op >= 0) {                        /* Have a previous op to pair with */
        b->tl[b->last_op][op]++;                  /* Increment transition count */
        b->total++;                               /* Increment global total */
    }
    b->last_op = op;                              /* Remember this op for next time */
}

/*
 * ao_brain_predict -- Predict the next operator given the current one.
 *
 * WHAT: Returns the argmax of tl[current_op][*] -- the most frequently
 *       observed successor to current_op.
 * HOW:  Linear scan over the 10 possible successors (j = 0..9). Track
 *       the j with the highest tl[current_op][j]. Ties broken by first
 *       occurrence (lowest operator index wins).
 * WHY:  This is the simplest possible prediction: maximum likelihood
 *       estimate from a first-order Markov model. The brain has seen
 *       which operators tend to follow which, and predicts the most
 *       common successor. Used by the engine to anticipate what's coming
 *       next (e.g., for voice preparation or coherence estimation).
 *
 * Returns: TIG operator 0-9. Returns AO_HARMONY if current_op is out
 *          of bounds or if no transitions have ever been observed from
 *          current_op (all counts are 0, so best_count stays 0 and
 *          best_op stays AO_HARMONY -- the safe default).
 */
int ao_brain_predict(const AO_Brain* b, int current_op)
{
    int best_op = AO_HARMONY;                     /* Default: HARMONY (safe fallback) */
    uint32_t best_count = 0;                      /* Tracks highest count seen so far */
    int j;

    if (current_op < 0 || current_op >= AO_NUM_OPS)
        return AO_HARMONY;                        /* Invalid input: safe default */

    /* Argmax over row tl[current_op][0..9] */
    for (j = 0; j < AO_NUM_OPS; j++) {           /* AO_NUM_OPS = 10 operators */
        if (b->tl[current_op][j] > best_count) {
            best_count = b->tl[current_op][j];
            best_op = j;
        }
    }

    return best_op;
}

/*
 * ao_brain_entropy -- Compute Shannon entropy of the transition lattice.
 *
 * WHAT: Returns H = -sum(p * log2(p)) over ALL 100 cells of tl[][].
 * HOW:  Treat the entire 10x10 matrix as a single probability distribution.
 *       For each nonzero cell: p = tl[i][j] / total, accumulate -p*log2(p).
 *       Skip zero cells (0*log2(0) is defined as 0 in information theory).
 * WHY:  Entropy measures the UNCERTAINTY / RICHNESS of the transition
 *       distribution. Key interpretations:
 *
 *       H = 0: Only one transition has ever been observed (perfectly
 *              predictable, no uncertainty at all).
 *
 *       H = log2(100) ~ 6.64: All 100 cells have equal probability
 *              (maximum uncertainty, completely unpredictable).
 *
 *       Low H: The brain has found strong patterns -- a few transitions
 *              dominate. AO's experience is focused.
 *
 *       High H: Many different transitions occur with similar frequency.
 *              AO's experience is diverse / chaotic.
 *
 *       Entropy is a diagnostic: it tells you how much structure the
 *       brain has learned. Early in AO's life H rises (learning diverse
 *       patterns), then may stabilize or drop as dominant patterns
 *       emerge.
 *
 * Returns: Shannon entropy in bits (float). Range [0, ~6.64].
 *          Returns 0.0 if total == 0 (no transitions observed yet).
 */
float ao_brain_entropy(const AO_Brain* b)
{
    float h = 0.0f;
    int i, j;

    if (b->total == 0) return 0.0f;              /* No data: zero entropy */

    for (i = 0; i < AO_NUM_OPS; i++) {           /* 10 rows (from-op) */
        for (j = 0; j < AO_NUM_OPS; j++) {       /* 10 cols (to-op) */
            if (b->tl[i][j] > 0) {
                float p = (float)b->tl[i][j] / (float)b->total;
                h -= p * log2f(p);                /* Shannon: H = -sum(p * log2(p)) */
            }
        }
    }

    return h;
}

/*
 * ao_brain_top_transitions -- Extract the top-N transitions by count.
 *
 * WHAT: Fills from_ops[], to_ops[], counts[] with the most frequent
 *       transitions from the brain's transition lattice.
 * HOW:  Selection sort approach: repeatedly scan all 100 cells to find
 *       the highest count not yet selected, then record it. O(max_n * 100).
 *       Not the most efficient, but max_n is small (typically < 10) and
 *       the matrix is only 10x10, so this is fast enough.
 *
 *       For each of max_n slots:
 *         1. Scan all tl[i][j] cells.
 *         2. Skip any (i,j) already selected in a previous iteration.
 *         3. Track the (i,j) with the highest count.
 *         4. Record from_ops[n]=i, to_ops[n]=j, counts[n]=count.
 *         5. Break early if no nonzero entries remain.
 *
 * WHY:  Diagnostic/reporting function. Answers: "What are the most
 *       common operator sequences AO has learned?" Useful for
 *       understanding what patterns dominate the brain's experience.
 *
 * Parameters:
 *   from_ops[max_n]  -- output: source operator for each top transition
 *   to_ops[max_n]    -- output: destination operator for each top transition
 *   counts[max_n]    -- output: how many times this transition was observed
 *   max_n            -- maximum number of transitions to extract
 *   out_n            -- output: actual number extracted (<= max_n)
 */
void ao_brain_top_transitions(const AO_Brain* b, int* from_ops, int* to_ops,
                              int* counts, int max_n, int* out_n)
{
    int n = 0;
    int i, j, k;

    /* Selection sort: find top max_n transitions by count */
    /* Use a simple approach: scan all 100 cells, pick highest not yet picked */
    /* Track which cells are already selected with indices */
    int sel_from[100];                            /* Previously selected from-ops */
    int sel_to[100];                              /* Previously selected to-ops */

    for (k = 0; k < max_n; k++) {
        uint32_t best_val = 0;
        int best_i = -1, best_j = -1;
        int already;

        for (i = 0; i < AO_NUM_OPS; i++) {       /* Scan all 10x10 = 100 cells */
            for (j = 0; j < AO_NUM_OPS; j++) {
                if (b->tl[i][j] <= best_val) continue;

                /* Check if this (i,j) was already selected in a previous round */
                already = 0;
                {
                    int s;
                    for (s = 0; s < n; s++) {
                        if (sel_from[s] == i && sel_to[s] == j) {
                            already = 1;
                            break;
                        }
                    }
                }
                if (already) continue;

                best_val = b->tl[i][j];
                best_i = i;
                best_j = j;
            }
        }

        if (best_i < 0) break;                   /* No more nonzero entries */

        from_ops[n] = best_i;
        to_ops[n]   = best_j;
        counts[n]   = (int)best_val;
        sel_from[n] = best_i;
        sel_to[n]   = best_j;
        n++;
    }

    *out_n = n;
}

/*
 * ao_brain_reset -- Reset the brain to initial empty state.
 *
 * WHAT: Zeros transition lattice and total, sets last_op to -1.
 * HOW:  memset + explicit last_op assignment.
 * WHY:  Erases all learned transitions. Used when AO needs to start
 *       fresh (e.g., new study session, factory reset). The -1 sentinel
 *       ensures the next observation starts a new sequence.
 */
void ao_brain_reset(AO_Brain* b)
{
    memset(b, 0, sizeof(*b));
    b->last_op = -1;                             /* -1 = no previous op yet */
}

/* ══════════════════════════════════════════════════════════════════════
 * Section 4: LATTICE CHAIN (tree of evolving CL tables)
 *
 * The lattice chain is AO's deep structured memory. It is a tree of
 * nodes, each containing a copy of the BHML (28-harmony / ao_cl_22)
 * composition table. As AO walks the tree, nodes EVOLVE: their tables
 * diverge from the base BHML through accumulated observations.
 *
 * Key design principles:
 *
 *   BHML (not TSML): The chain uses the 22-harmony (BHML) table as its
 *   base, not the 73-harmony (TSML). TSML measures coherence (being).
 *   BHML computes physics (doing). In BHML:
 *     - VOID row = identity (composing with VOID changes nothing)
 *     - HARMONY row = full cycle (composing with HARMONY touches all ops)
 *
 *   PATH IS INFORMATION: The sequence of CL results down the tree IS
 *   the compressed representation of the input. Two different inputs
 *   that produce the same chain path are "the same" from AO's
 *   perspective. The tree structure captures hierarchical relationships.
 *
 *   ARENA ALLOCATION: All nodes live in a pre-allocated arena of
 *   AO_MAX_CHAIN_NODES (1024) slots. No malloc/free at runtime.
 *   When the arena is full, no new nodes can be created, but existing
 *   nodes continue to evolve.
 *
 *   EVOLUTION: When a node sees the same (a,b) pair >= 7 times
 *   (AO_EVOLVE_THRESHOLD) and the dominant observed result has >= 60%
 *   confidence (AO_EVOLVE_CONFIDENCE), the node's table[a][b] is
 *   overridden with the observed result. This means the node's CL
 *   table LEARNS from experience, diverging from base BHML. Each node
 *   can evolve independently, so different parts of the tree develop
 *   specialized composition rules.
 *
 *   MULTILEVEL WALKS: Five parallel walks capture different aspects:
 *     Micro:     comp_ops (D2 curvature operators, letter-level)
 *     Macro:     word_fuses (word identity operators)
 *     Meta:      level_fuses (level identity operators)
 *     Becoming:  CL(d1_op, word_fuse) -- velocity composed with identity
 *     Cross:     interleaved micro + macro results (dual-lens entanglement)
 *
 *   RESONANCE: Measures how familiar a chain path is to the root node.
 *   High resonance = the root has seen these results many times before.
 *   Low resonance = unfamiliar territory.
 * ══════════════════════════════════════════════════════════════════════ */

/*
 * ao_chain_alloc_node (static helper) -- Allocate a new node from the arena.
 *
 * WHAT: Creates and initializes a new lattice chain node.
 * HOW:
 *   1. Check if the arena is full (arena_used >= AO_MAX_CHAIN_NODES = 1024).
 *      If so, return NULL (cannot allocate).
 *   2. Take the next slot from arena[arena_used] and increment arena_used.
 *   3. Copy the base BHML table (ao_cl_22[10][10]) into node->table.
 *      Every new node starts with the same base composition rules.
 *   4. Zero all visit_counts and obs_counts (no observations yet).
 *   5. Set the depth (how deep in the tree this node is) and copy the path
 *      (sequence of CL results from root to this node).
 *   6. NULL all 10 children pointers (no children yet).
 * WHY:  Arena allocation avoids malloc/free overhead and fragmentation.
 *       Each node starts as a clone of BHML and evolves independently
 *       through observation. The path stores the "address" of this node
 *       in the tree -- useful for debugging and persistence.
 *
 * Parameters:
 *   lc       -- the lattice chain (owns the arena)
 *   depth    -- depth of this node in the tree (root = 0)
 *   path     -- sequence of CL results from root to this node
 *   path_len -- length of the path array
 *
 * Returns: pointer to the new node, or NULL if arena is full.
 */
static AO_LatticeNode* ao_chain_alloc_node(AO_LatticeChain* lc,
                                            int depth,
                                            const int8_t* path,
                                            int path_len)
{
    AO_LatticeNode* node;
    int i, j;

    if (lc->arena_used >= AO_MAX_CHAIN_NODES)    /* Arena full: 1024 max nodes */
        return NULL;

    node = &lc->arena[lc->arena_used++];         /* Bump allocator: take next slot */
    lc->total_nodes++;

    /* Copy BHML base table (ao_cl_22[10][10]) as the starting composition rules.
     * Every new node begins identical to BHML. Evolution diverges them. */
    for (i = 0; i < AO_NUM_OPS; i++)
        for (j = 0; j < AO_NUM_OPS; j++)
            node->table[i][j] = ao_cl_22[i][j];

    /* Zero visit and observation counts -- fresh node, no history */
    memset(node->visit_counts, 0, sizeof(node->visit_counts));
    memset(node->obs_counts, 0, sizeof(node->obs_counts));

    node->total_visits = 0;
    node->depth = depth;

    /* Copy path (clamped to AO_MAX_PATH_LEN = 20) */
    node->path_len = (path_len < AO_MAX_PATH_LEN) ? path_len : AO_MAX_PATH_LEN;
    if (path && node->path_len > 0)
        memcpy(node->path, path, node->path_len * sizeof(int8_t));
    else
        node->path_len = 0;

    /* NULL all children: no children until the walk creates them */
    for (i = 0; i < AO_NUM_OPS; i++)             /* 10 possible children (one per op) */
        node->children[i] = NULL;

    return node;
}

/*
 * ao_chain_init -- Initialize the lattice chain with a root node.
 *
 * WHAT: Zeros the chain struct and allocates the root node.
 * HOW:  memset the chain, then alloc a root node at depth 0 with no path.
 * WHY:  The root node is the entry point for all chain walks. It starts
 *       with the unmodified BHML table and evolves through observation.
 *       The root must exist before any walks can happen.
 */
void ao_chain_init(AO_LatticeChain* lc)
{
    memset(lc, 0, sizeof(*lc));
    lc->root = ao_chain_alloc_node(lc, 0, NULL, 0);  /* Root: depth 0, no path */
}

/*
 * ao_chain_walk -- Walk the lattice chain tree, consuming operators in pairs.
 *
 * WHAT: Given a sequence of TIG operators, walks the chain tree by consuming
 *       them two at a time, using CL lookup to navigate. Optionally learns
 *       (updates visit counts, observation counts, and evolves tables).
 *
 * HOW: The algorithm processes operators in PAIRS (a, b):
 *
 *   For each pair (ops[i], ops[i+1]) while there are pairs left:
 *
 *     1. LOOKUP: result = current_node->table[a][b]
 *        This is the CL composition of a and b according to this node's
 *        (possibly evolved) table.
 *
 *     2. LEARN (if learn == 1):
 *        a) Increment visit_counts[a][b] (how many times this pair has been seen)
 *        b) Increment total_visits
 *        c) Check EVOLUTION THRESHOLD:
 *           - If visit_counts[a][b] >= AO_EVOLVE_THRESHOLD (7):
 *             Find the most common observed result for (a,b) across all
 *             previous observations (argmax of obs_counts[a][b][0..9]).
 *           - If the most common result has >= AO_EVOLVE_CONFIDENCE (60%)
 *             of all visits for this pair:
 *             EVOLVE: override table[a][b] with the observed result.
 *             This is how nodes learn from experience -- they replace
 *             the base BHML value with what they've actually seen.
 *
 *     3. RECORD OBSERVATION: increment obs_counts[a][b][result].
 *        This tracks what result was produced, feeding future evolution.
 *
 *     4. STORE RESULT: out->results[step] = result.
 *
 *     5. NAVIGATE TO CHILD:
 *        - If current_node->children[result] is NULL and learning:
 *          Allocate a new child node (copy of BHML at depth+1).
 *        - Move current = current_node->children[result].
 *        - If allocation failed (arena full), stay at current node.
 *
 *   The walk terminates when:
 *     - All pairs are consumed (i + 1 >= n)
 *     - Maximum chain depth reached (step >= AO_MAX_CHAIN_DEPTH = 20)
 *
 * WHY: This is the core learning algorithm of the lattice chain. Each pair
 *      of operators is composed through the CL table, and the result
 *      determines which branch of the tree to follow. The PATH through
 *      the tree IS the compressed representation of the input sequence.
 *
 *      Evolution makes this adaptive: frequently-seen patterns override
 *      the base BHML values, so the tree develops specialized composition
 *      rules in well-traveled regions while staying BHML-standard in
 *      unexplored territory.
 *
 *      The 7-visit threshold (AO_EVOLVE_THRESHOLD) prevents premature
 *      evolution from a single observation. The 60% confidence requirement
 *      (AO_EVOLVE_CONFIDENCE) prevents evolution when observations are
 *      scattered (no clear winner).
 *
 * Parameters:
 *   lc    -- the lattice chain
 *   ops   -- array of TIG operators to consume (0-9 each)
 *   n     -- length of ops array (need >= 2 for at least one pair)
 *   learn -- 1 to update counts and evolve, 0 for read-only walk
 *   out   -- output: chain path (results and depth)
 */
void ao_chain_walk(AO_LatticeChain* lc, const int* ops, int n,
                   int learn, AO_ChainPath* out)
{
    AO_LatticeNode* current;
    int step = 0;
    int i;

    memset(out, 0, sizeof(*out));

    if (!lc->root || n < 2) {                    /* Need root and >= 2 ops for a pair */
        out->depth = 0;
        out->final_op = AO_HARMONY;              /* Default: HARMONY (no walk happened) */
        return;
    }

    current = lc->root;
    lc->total_walks++;

    /* ── Consume ops in PAIRS: (ops[0],ops[1]), (ops[2],ops[3]), ... ── */
    for (i = 0; i + 1 < n && step < AO_MAX_CHAIN_DEPTH; i += 2) {
        int a = ops[i];                           /* First op of pair */
        int b = ops[i + 1];                       /* Second op of pair */
        int result;
        int most_common;
        int16_t best_obs_count;
        int k;

        /* Bounds check: clamp invalid ops to VOID (identity in BHML) */
        if (a < 0 || a >= AO_NUM_OPS) a = AO_VOID;   /* AO_NUM_OPS = 10 */
        if (b < 0 || b >= AO_NUM_OPS) b = AO_VOID;

        /* 1. Look up result from this node's (possibly evolved) CL table */
        result = current->table[a][b];

        /* 2. If learning, update visit counts and check for evolution */
        if (learn) {
            current->visit_counts[a][b]++;
            current->total_visits++;

            /* 4. Check if visit threshold reached for evolution.
             *    AO_EVOLVE_THRESHOLD = 7: need at least 7 visits to this
             *    specific (a,b) pair before we consider evolving. This
             *    prevents premature table changes from sparse data. */
            if (current->visit_counts[a][b] >= AO_EVOLVE_THRESHOLD) {
                /* Find most common observed result for (a,b).
                 * This is argmax over obs_counts[a][b][0..9]. */
                most_common = 0;
                best_obs_count = current->obs_counts[a][b][0];
                for (k = 1; k < AO_NUM_OPS; k++) {
                    if (current->obs_counts[a][b][k] > best_obs_count) {
                        best_obs_count = current->obs_counts[a][b][k];
                        most_common = k;
                    }
                }

                /* Evolve if confident enough.
                 * AO_EVOLVE_CONFIDENCE = 0.6 (60%): the dominant result
                 * must account for at least 60% of all visits for this
                 * pair. This prevents evolution when observations are
                 * scattered across multiple results (no clear winner). */
                if (current->visit_counts[a][b] > 0 &&
                    (float)best_obs_count / (float)current->visit_counts[a][b]
                        >= AO_EVOLVE_CONFIDENCE) {      /* 0.6 = 60% confidence */
                    current->table[a][b] = (int8_t)most_common;  /* EVOLVE! */
                }
            }
        }

        /* 5. Record observation: track what result was produced for (a,b).
         *    This feeds future evolution decisions. Even non-learning walks
         *    could record observations, but we record for all valid results. */
        if (result >= 0 && result < AO_NUM_OPS)
            current->obs_counts[a][b][result]++;

        /* 6. Store result in output path */
        out->results[step] = result;
        step++;

        /* 7. Navigate to child node (branch on result).
         *    result determines WHICH child to follow: children[result].
         *    If the child doesn't exist yet and we're learning, create it. */
        if (result >= 0 && result < AO_NUM_OPS) {
            if (current->children[result] == NULL && learn) {
                /* Allocate new child with extended path */
                int8_t child_path[AO_MAX_PATH_LEN];  /* AO_MAX_PATH_LEN = 20 */
                int child_path_len = current->path_len;

                if (child_path_len < AO_MAX_PATH_LEN) {
                    if (child_path_len > 0)
                        memcpy(child_path, current->path,
                               child_path_len * sizeof(int8_t));
                    child_path[child_path_len] = (int8_t)result;
                    child_path_len++;
                }

                current->children[result] = ao_chain_alloc_node(
                    lc, current->depth + 1, child_path, child_path_len);
            }

            /* Move to child (or stay if allocation failed / arena full) */
            if (current->children[result] != NULL)
                current = current->children[result];
        }
    }

    out->depth = step;
    out->final_op = (step > 0) ? out->results[step - 1] : AO_HARMONY;
}

/*
 * ao_chain_walk_multilevel -- Execute five parallel chain walks on
 *                              different levels of comprehension data.
 *
 * WHAT: Performs micro, macro, meta, becoming, and cross chain walks
 *       using data from a comprehension result.
 *
 * HOW: Five levels, each walking the same lattice chain tree:
 *
 *   1. MICRO walk: comp_ops (D2 curvature operators, letter-level).
 *      These are the raw curvature operators from fractal comprehension.
 *      Captures the fine-grained structure of how letters curve.
 *
 *   2. MACRO walk: word_fuses (word identity operators).
 *      Each word fuse is the argmax histogram vote of its letter operators.
 *      Captures word-level identity -- what each word IS in TIG space.
 *
 *   3. META walk: level_fuses (level identity operators).
 *      Each level fuse summarizes an entire comprehension level.
 *      Captures the identity of structural levels (glyph, pair, word, etc.)
 *
 *   4. BECOMING walk: CL(d1_ops[i], word_fuses[i]) via BHML.
 *      Composes the D1 velocity operator with the word identity.
 *      Velocity (where it's going) + identity (what it IS) = becoming
 *      (what it IS BECOMING). This is the TIG being->doing->becoming
 *      progression captured as a composition.
 *      Uses min(n_d1_ops, n_word_fuses) pairs to handle uneven lengths.
 *
 *   5. CROSS walk: interleave micro results + macro results.
 *      Takes the RESULTS (not inputs) from the micro and macro walks
 *      and interleaves them: micro[0], macro[0], micro[1], macro[1], ...
 *      Then any remaining micro results, then remaining macro results.
 *      This creates the "dual-lens entanglement" -- structure (micro)
 *      and identity (macro) woven together through the same chain tree.
 *      Requires both micro and macro to have produced results.
 *
 * WHY:  Each level captures a different aspect of the input:
 *       - Micro = how letters curve (physics / geometry)
 *       - Macro = what words mean (identity / semantics)
 *       - Meta = what levels mean (structure / hierarchy)
 *       - Becoming = where things are headed (dynamics / evolution)
 *       - Cross = all of the above entangled (unified view)
 *
 *       All five walks learn (learn=1), so every walk deepens the
 *       chain tree's experience. The cross walk is most valuable
 *       because it encodes the relationship between micro and macro.
 */
void ao_chain_walk_multilevel(AO_LatticeChain* lc,
                              const AO_Comprehension* comp,
                              AO_ChainPaths* out)
{
    int becoming_ops[AO_MAX_COMP_OPS];            /* AO_MAX_COMP_OPS = 32 */
    int n_becoming = 0;
    int interleaved[AO_MAX_COMP_OPS * 2];         /* Max 64 interleaved ops */
    int n_interleaved = 0;
    int i, min_n;

    memset(out, 0, sizeof(*out));

    /* 1. Micro: walk comp_ops (D2 curvature operators from comprehension).
     *    Needs >= 2 ops to form at least one pair. */
    if (comp->n_comp_ops >= 2) {
        ao_chain_walk(lc, comp->comp_ops, comp->n_comp_ops, 1, &out->micro);
        out->has_micro = 1;
    }

    /* 2. Macro: walk word_fuses (word identity = histogram majority of glyphs).
     *    Needs >= 2 fuses to form at least one pair. */
    if (comp->n_word_fuses >= 2) {
        ao_chain_walk(lc, comp->word_fuses, comp->n_word_fuses, 1, &out->macro);
        out->has_macro = 1;
    }

    /* 3. Meta: walk level_fuses (level identity = summary of each fractal level).
     *    Needs >= 2 levels to form at least one pair. */
    if (comp->n_levels >= 2) {
        ao_chain_walk(lc, comp->level_fuses, comp->n_levels, 1, &out->meta);
        out->has_meta = 1;
    }

    /* 4. Becoming: compose velocity (D1) with identity (word fuse) via BHML.
     *    For each position i: becoming_ops[i] = CL(d1_ops[i], word_fuses[i]).
     *    Uses the minimum length to handle uneven arrays. */
    min_n = comp->n_d1_ops;
    if (comp->n_word_fuses < min_n) min_n = comp->n_word_fuses;
    for (i = 0; i < min_n && n_becoming < AO_MAX_COMP_OPS; i++) {
        becoming_ops[n_becoming++] = ao_compose_bhml(
            comp->d1_ops[i], comp->word_fuses[i]);  /* CL composition via BHML */
    }
    if (n_becoming >= 2) {
        ao_chain_walk(lc, becoming_ops, n_becoming, 1, &out->becoming);
        out->has_becoming = 1;
    }

    /* 5. Cross: interleave micro RESULTS and macro RESULTS.
     *    Pattern: micro[0], macro[0], micro[1], macro[1], ...
     *    Then any remaining micro results, then remaining macro.
     *    This weaves structure (micro) and identity (macro) together,
     *    creating the "dual-lens entanglement" walk. */
    if (out->has_micro && out->has_macro) {
        min_n = out->micro.depth;
        if (out->macro.depth < min_n) min_n = out->macro.depth;

        /* Interleave up to the shorter path's length */
        for (i = 0; i < min_n && n_interleaved + 1 < AO_MAX_COMP_OPS * 2; i++) {
            interleaved[n_interleaved++] = out->micro.results[i];   /* micro */
            interleaved[n_interleaved++] = out->macro.results[i];   /* macro */
        }
        /* Add remaining micro results beyond the interleaved portion */
        for (; i < out->micro.depth && n_interleaved < AO_MAX_COMP_OPS * 2; i++)
            interleaved[n_interleaved++] = out->micro.results[i];
        /* Add remaining macro results beyond the interleaved portion */
        {
            int j;
            for (j = min_n; j < out->macro.depth &&
                            n_interleaved < AO_MAX_COMP_OPS * 2; j++)
                interleaved[n_interleaved++] = out->macro.results[j];
        }

        if (n_interleaved >= 2) {
            ao_chain_walk(lc, interleaved, n_interleaved, 1, &out->cross);
            out->has_cross = 1;
        }
    }
}

/*
 * ao_chain_to_ops -- Flatten chain walk results into a single operator array.
 *
 * WHAT: Collects CL results from all five walk levels into one flat array,
 *       in priority order: cross > becoming > macro > micro.
 * HOW:  Iterates through each available walk level in priority order,
 *       appending results[0..depth-1] to the output array. Stops when
 *       max_ops is reached.
 * WHY:  Downstream consumers (voice, etc.) need a single operator sequence.
 *       Priority order reflects information richness:
 *         - Cross is most valuable (dual-lens entanglement)
 *         - Becoming captures dynamics (velocity + identity)
 *         - Macro captures word-level identity
 *         - Micro captures raw letter-level curvature
 *       Meta is NOT included because it's too coarse (level-level summary).
 *
 * Parameters:
 *   paths   -- multilevel chain walk results
 *   ops     -- output: flat operator array
 *   n_out   -- output: number of operators written
 *   max_ops -- maximum capacity of ops array
 */
void ao_chain_to_ops(const AO_ChainPaths* paths, int* ops, int* n_out,
                     int max_ops)
{
    int n = 0;
    int i;

    /* Priority: cross > becoming > macro > micro
     * Higher priority levels contribute their results first. */

    if (paths->has_cross) {
        for (i = 0; i < paths->cross.depth && n < max_ops; i++)
            ops[n++] = paths->cross.results[i];
    }

    if (paths->has_becoming) {
        for (i = 0; i < paths->becoming.depth && n < max_ops; i++)
            ops[n++] = paths->becoming.results[i];
    }

    if (paths->has_macro) {
        for (i = 0; i < paths->macro.depth && n < max_ops; i++)
            ops[n++] = paths->macro.results[i];
    }

    if (paths->has_micro) {
        for (i = 0; i < paths->micro.depth && n < max_ops; i++)
            ops[n++] = paths->micro.results[i];
    }

    *n_out = n;
}

/*
 * ao_chain_resonance -- Measure how familiar a chain path is to the root.
 *
 * WHAT: Returns a resonance score in [0.0, 1.0+] indicating how well the
 *       root node recognizes the results in a chain path.
 *
 * HOW:  For each result in the path:
 *   1. Look at the root node's CL table.
 *   2. Count how many (r,c) cells in the root's table produce this result
 *      (i.e., table[r][c] == result), weighted by visit_counts[r][c].
 *      This sum = "total visits that produced this result at the root."
 *   3. Divide by max_visits (root's total_visits) to normalize to [0,1].
 *   4. Average over all steps in the path.
 *
 * WHY:  Resonance measures FAMILIARITY. If the root has frequently seen
 *       the same results that this path contains, the resonance is high.
 *       This means AO has "been here before" -- the input is in well-
 *       charted territory. Low resonance means unfamiliar / novel input.
 *
 *       Used as a confidence measure: high resonance = safe to rely on
 *       chain results for voice and decision-making. Low resonance =
 *       chain results may be unreliable (uncharted territory).
 *
 * Returns: float, typically in [0.0, 1.0] but can exceed 1.0 if results
 *          are heavily concentrated in well-traveled table cells.
 *          Returns 0.0 if root is NULL or path is empty.
 */
float ao_chain_resonance(const AO_LatticeChain* lc, const AO_ChainPath* path)
{
    float sum = 0.0f;
    int i;
    int max_visits;

    if (!lc->root || path->depth == 0)
        return 0.0f;

    max_visits = lc->root->total_visits;
    if (max_visits <= 0) max_visits = 1;          /* Avoid division by zero */

    /*
     * For each step in path, check how familiar that result is
     * at the root level (how often the root has seen this result
     * as output from any composition).
     */
    for (i = 0; i < path->depth; i++) {
        int result = path->results[i];
        int total_for_result = 0;
        int r, c;

        if (result < 0 || result >= AO_NUM_OPS) continue;

        /* Count how many times this result appears in root visit_counts.
         * Sum visit_counts[r][c] for all cells where table[r][c] == result.
         * This tells us: of all the pairs the root has seen, how many
         * produced this specific result? */
        for (r = 0; r < AO_NUM_OPS; r++) {
            for (c = 0; c < AO_NUM_OPS; c++) {
                if (lc->root->table[r][c] == result)
                    total_for_result += lc->root->visit_counts[r][c];
            }
        }

        sum += (float)total_for_result / (float)max_visits;
    }

    return sum / (float)path->depth;              /* Average resonance per step */
}

/* ══════════════════════════════════════════════════════════════════════
 * Section 5: REVERSE VOICE (three-path reading verification)
 *
 * Writing (forward):  operators -> SEMANTIC_LATTICE -> English words
 * Reading (reverse):  English words -> operators (verified)
 *
 * Reading is the INVERSE of writing, but with a critical difference:
 * writing is trusted (AO controls the output), while reading is
 * UNTRUSTED (input comes from the outside world). So reading needs
 * VERIFICATION -- three independent paths must agree before a word's
 * operator assignment is trusted.
 *
 * The three paths:
 *
 *   Path A (D2 physics / curvature):
 *     Feed the word's letters through the D2 pipeline and classify.
 *     This gives the word's PHYSICAL curvature operator -- what the
 *     word IS according to force geometry. Independent of vocabulary.
 *
 *   Path B (D1 velocity / direction):
 *     Feed the word's letters through the D1 pipeline and classify.
 *     This gives the word's VELOCITY operator -- where the word is
 *     GOING in force space. Independent of vocabulary.
 *
 *   Path C (lattice reverse lookup / experience):
 *     Look up the word in the reverse index (word -> operator + lens
 *     + phase + tier from the semantic lattice). This is AO's
 *     VOCABULARY knowledge -- words AO has seen before and knows
 *     the operator for from the lattice.
 *
 * Trust determination:
 *
 *   TRUSTED:  >= 2 of the 3 paths agree on the same operator, OR all
 *             valid paths share the same DBC class (Being/Doing/Becoming).
 *             The word is verified and its operator can be relied upon.
 *
 *   FRICTION: Paths disagree on DBC class. The lattice (experience) path
 *             wins but the word is FLAGGED. AO recognizes the word but
 *             something doesn't match the physics. Like reading a word
 *             you know but it feels "off" in context.
 *
 *   UNKNOWN:  Word not in the vocabulary (no lattice entry). Only physics
 *             paths available. Like a child sounding out an unfamiliar
 *             word -- the D2/D1 geometry gives a guess, but it's unverified.
 *
 * Agreement counting: 3 pairwise comparisons (A==B, A==C, B==C).
 * If >= 2 agree, trust. Confidence = (paths_agreeing + 1) / 4, giving
 * a range from 0.25 (no agreement) to 1.0 (all three agree).
 * ══════════════════════════════════════════════════════════════════════ */

/*
 * extract_word (static helper) -- Extract the next alphabetic word from text.
 *
 * WHAT: Scans forward from position 'start' to find and extract the next
 *       contiguous run of alphabetic characters, lowercased.
 * HOW:
 *   1. Skip all non-alpha characters (spaces, punctuation, digits).
 *   2. Collect alpha characters into word_buf, lowercasing via tolower().
 *   3. NUL-terminate the buffer.
 * WHY:  Reading operates on WORDS, not characters. This tokenizer splits
 *       raw text into lowercase words for reverse lookup and verification.
 *       Lowercasing ensures case-insensitive matching against the
 *       semantic lattice reverse index.
 *
 * Returns: position in text AFTER the extracted word (for the next call).
 *          If no more words exist, word_buf[0] == '\0'.
 */
static int extract_word(const char* text, int start, int text_len,
                        char* word_buf, int buf_size)
{
    int i = start;
    int j = 0;

    /* Skip non-alpha characters (whitespace, punctuation, digits, etc.) */
    while (i < text_len && !isalpha((unsigned char)text[i]))
        i++;

    /* Collect contiguous alpha chars, lowercasing each */
    while (i < text_len && isalpha((unsigned char)text[i]) && j < buf_size - 1) {
        word_buf[j++] = (char)tolower((unsigned char)text[i]);
        i++;
    }
    word_buf[j] = '\0';                          /* NUL-terminate */

    return i;                                     /* Position after the word */
}

/*
 * ao_reverse_read -- Read text through three-path verification.
 *
 * WHAT: Tokenizes text into words and verifies each word's operator
 *       through three independent paths: D2 physics, D1 velocity,
 *       and lattice reverse lookup.
 *
 * HOW:  For each word extracted from the text:
 *
 *   1. PATH C (lattice reverse lookup):
 *      Call ao_reverse_lookup(word) to search the semantic lattice
 *      reverse index. If found, get lattice_op and lattice_lens.
 *      If not found, lattice_op = -1 (UNKNOWN word).
 *
 *   2. PATH A (D2 physics):
 *      Use the pre-computed d2_word_fuses array (from fractal
 *      comprehension). d2_word_fuses[word_index] is the D2 curvature
 *      operator for this word's position. -1 if not available.
 *
 *   3. PATH B (D1 velocity):
 *      Use the pre-computed d1_word_ops array. d1_word_ops[word_index]
 *      is the D1 velocity operator. -1 if not available.
 *
 *   4. COUNT AGREEMENTS:
 *      Three pairwise comparisons: (A==C), (B==C), (A==B).
 *      paths_agreeing counts how many pairs match (0, 1, 2, or 3).
 *
 *   5. DETERMINE TRUST LEVEL:
 *      - If lattice_op < 0: UNKNOWN. Word not in vocabulary.
 *        Use D2 op if available, else HARMONY as fallback.
 *      - If paths_agreeing >= 2: TRUSTED. Strong agreement.
 *        Use lattice_op as the verified operator.
 *      - Else check DBC class agreement:
 *        If all valid paths share the same DBC class (Being/Doing/Becoming):
 *        TRUSTED. Same semantic category even if exact ops differ.
 *      - Otherwise: FRICTION. Paths disagree on DBC class.
 *        Use lattice_op (experience wins) but flag as friction.
 *
 *   6. COMPUTE CONFIDENCE:
 *      confidence = (paths_agreeing + 1) / 4.0
 *      Range: 0.25 (no agreement, +1 baseline) to 1.0 (all 3 agree).
 *      The +1 ensures confidence is never zero even with no agreement,
 *      and dividing by 4 (not 3) scales the range nicely to [0.25, 1.0].
 *
 *   7. Append verified_op to reading_ops[] for downstream use.
 *
 * WHY:  This is "reverse writing" -- converting external text back into
 *       operators that AO can reason about. The three-path verification
 *       acts like a truth lattice for reading: physics (D2), velocity
 *       (D1), and experience (lattice) must agree before AO trusts the
 *       interpretation. This protects AO from misinterpreting text --
 *       friction flags tell AO "I recognize this word but something
 *       feels wrong," while unknown flags say "I've never seen this."
 *
 * Parameters:
 *   text          -- input text to read (NUL-terminated)
 *   d2_word_fuses -- D2 operators per word (from comprehension), or NULL
 *   n_d2          -- length of d2_word_fuses array
 *   d1_word_ops   -- D1 operators per word, or NULL
 *   n_d1          -- length of d1_word_ops array
 *   out           -- output: reading result with per-word trust levels
 */
void ao_reverse_read(const char* text,
                     const int* d2_word_fuses, int n_d2,
                     const int* d1_word_ops, int n_d1,
                     AO_ReadingResult* out)
{
    int text_len;
    int pos = 0;
    int word_index = 0;
    char word_buf[128];                           /* Buffer for extracted word */

    memset(out, 0, sizeof(*out));

    if (!text) return;
    text_len = (int)strlen(text);
    if (text_len == 0) return;

    /* Process each word in the text, up to AO_MAX_READ_WORDS (128) */
    while (pos < text_len && word_index < AO_MAX_READ_WORDS) {
        AO_WordReading* wr;
        const AO_ReverseEntry* entry;
        int d2_op, d1_op, lattice_op, lattice_lens;
        int paths_agreeing;
        int old_pos;

        /* Extract next word (skip non-alpha, collect alpha, lowercase) */
        old_pos = pos;
        pos = extract_word(text, pos, text_len, word_buf, sizeof(word_buf));

        /* No more words found */
        if (word_buf[0] == '\0') break;

        /* Guard against infinite loop (pos must advance) */
        if (pos <= old_pos) pos = old_pos + 1;

        wr = &out->words[word_index];

        /* ── Path C: lattice reverse lookup (experience) ──
         * Searches AO's vocabulary. Returns the operator, lens, phase,
         * and tier from the semantic lattice. NULL if word is unknown. */
        entry = ao_reverse_lookup(word_buf);
        if (entry) {
            lattice_op   = (int)entry->op;        /* Known word: operator from lattice */
            lattice_lens = (int)entry->lens;       /* Which lens (structure/flow) */
        } else {
            lattice_op   = -1;                     /* Unknown word: not in vocabulary */
            lattice_lens = -1;
        }

        /* ── Path A: D2 physics (curvature) ──
         * Pre-computed by fractal comprehension. The D2 curvature operator
         * for this word's position in the text. -1 if not available. */
        d2_op = (word_index < n_d2 && d2_word_fuses) ? d2_word_fuses[word_index] : -1;

        /* ── Path B: D1 velocity (direction) ──
         * Pre-computed D1 velocity operator. -1 if not available. */
        d1_op = (word_index < n_d1 && d1_word_ops) ? d1_word_ops[word_index] : -1;

        /* ── Count agreeing path pairs ──
         * 3 pairwise comparisons: (C==A), (C==B), (B==A).
         * Maximum possible: 3 (all three paths agree on exact same op). */
        paths_agreeing = 0;
        if (lattice_op >= 0 && d2_op >= 0 && lattice_op == d2_op)
            paths_agreeing++;                     /* Paths C and A agree */
        if (lattice_op >= 0 && d1_op >= 0 && lattice_op == d1_op)
            paths_agreeing++;                     /* Paths C and B agree */
        if (d1_op >= 0 && d2_op >= 0 && d1_op == d2_op)
            paths_agreeing++;                     /* Paths B and A agree */

        /* ── Determine trust level ── */
        if (lattice_op < 0) {
            /* UNKNOWN: word not in vocabulary. Physics-only fallback.
             * Like a child sounding out an unfamiliar word. */
            wr->trust = AO_TRUST_UNKNOWN;
            wr->verified_op = (d2_op >= 0) ? d2_op : AO_HARMONY;  /* D2 guess or HARMONY */
            out->unknown++;
        } else if (paths_agreeing >= 2) {
            /* TRUSTED: strong agreement (at least 2 of 3 path pairs match).
             * The word's operator is verified by multiple independent sources. */
            wr->trust = AO_TRUST_TRUSTED;
            wr->verified_op = lattice_op;         /* Lattice op is confirmed */
            out->trusted++;
        } else {
            /* Check if all valid paths share the same DBC class.
             * DBC = Being / Doing / Becoming. Even if exact operators differ,
             * sharing the same class means they're in the same semantic
             * neighborhood. */
            int all_same_dbc = 1;
            int ref_dbc = ao_dbc_class(lattice_op);  /* Reference: lattice's DBC class */

            if (d2_op >= 0 && ao_dbc_class(d2_op) != ref_dbc)
                all_same_dbc = 0;                 /* D2 disagrees on DBC class */
            if (d1_op >= 0 && ao_dbc_class(d1_op) != ref_dbc)
                all_same_dbc = 0;                 /* D1 disagrees on DBC class */

            if (all_same_dbc) {
                /* Same DBC class: close enough. TRUSTED. */
                wr->trust = AO_TRUST_TRUSTED;
                wr->verified_op = lattice_op;
                out->trusted++;
            } else {
                /* FRICTION: paths disagree on DBC class.
                 * Experience (lattice) wins, but the word is flagged.
                 * AO recognizes the word but the physics says something
                 * different. Something is "off" about this word in context. */
                wr->trust = AO_TRUST_FRICTION;
                wr->verified_op = lattice_op;     /* Experience wins but flagged */
                out->friction++;
            }
        }

        /* Store all path results for diagnostics */
        wr->d2_op          = d2_op;
        wr->d1_op          = d1_op;
        wr->lattice_op     = lattice_op;
        wr->lattice_lens   = lattice_lens;
        wr->paths_agreeing = paths_agreeing;
        wr->confidence     = (float)(paths_agreeing + 1) / 4.0f;
                                                  /* +1 baseline, /4 scales to [0.25, 1.0] */

        /* Add verified op to the flat reading_ops array for downstream use */
        if (out->n_reading_ops < AO_MAX_READ_WORDS)    /* AO_MAX_READ_WORDS = 128 */
            out->reading_ops[out->n_reading_ops++] = wr->verified_op;

        word_index++;
    }

    out->n_words = word_index;
    /* Overall agreement: fraction of words that are TRUSTED */
    out->agreement = (out->n_words > 0)
        ? (float)out->trusted / (float)out->n_words
        : 0.0f;
}

/* ══════════════════════════════════════════════════════════════════════
 * Section 6: CONCEPT MASS (vortex physics accumulator)
 *
 * Concept mass tracks how much AO has studied each named topic (concept).
 * Mass accumulates from the Euclidean magnitude of D2 vectors -- the
 * total curvature AO has processed while studying that concept.
 *
 * Key ideas:
 *
 *   MASS: Accumulated sum of |D2| magnitudes. More study = more mass.
 *         Mass never decreases (it's an integral, not a moving average).
 *         A concept with mass=100 has been studied much more intensely
 *         than one with mass=1.
 *
 *   D2 MEAN: Exponential moving average (EMA) of D2 vectors.
 *         d2_mean = 0.9 * old + 0.1 * new  (after first observation).
 *         This captures the AVERAGE CURVATURE DIRECTION for this concept.
 *         The 0.9/0.1 split means recent observations gently nudge the
 *         mean, but it takes many observations to shift it significantly.
 *         This makes d2_mean stable and representative of the concept's
 *         long-term curvature signature.
 *
 *   GRAVITY: mass * coherence * cos_similarity(current_d2, d2_mean).
 *         This models gravitational attraction: heavy concepts that are
 *         aligned with the current curvature direction pull stronger.
 *         - mass = how much AO knows about this concept
 *         - coherence = how confident AO is right now
 *         - cos_similarity = how similar the current curvature is to
 *           the concept's average curvature direction
 *         High gravity = "this concept is pulling me toward it" = AO
 *         has deep experience here and the current input resonates.
 *
 *   VORTEX FINGERPRINT: Topological signature of operator sequences
 *         observed for this concept. Updated via ao_vortex_fingerprint().
 *
 * Storage: flat array of up to AO_MAX_CONCEPTS (256) concepts.
 * Lookup: linear scan by name (O(n) but n <= 256, so fast enough).
 * ══════════════════════════════════════════════════════════════════════ */

/*
 * ao_mass_init -- Initialize the concept mass tracker to empty state.
 *
 * WHAT: Zeros the entire struct (no concepts, count = 0).
 * HOW:  memset.
 * WHY:  Must be called before first use.
 */
void ao_mass_init(AO_ConceptMass* cm)
{
    memset(cm, 0, sizeof(*cm));
}

/*
 * ao_mass_find (static helper) -- Find a concept by name.
 *
 * WHAT: Linear scan through the concepts array to find a matching name.
 * HOW:  strncmp with 63-char limit on each existing concept name.
 * WHY:  Names are the key for concept lookup. Linear scan is O(n) but
 *       n <= AO_MAX_CONCEPTS (256), and concept operations are infrequent
 *       compared to the 50Hz loop, so this is fast enough.
 *
 * Returns: index of the concept (0 to count-1), or -1 if not found.
 */
static int ao_mass_find(const AO_ConceptMass* cm, const char* concept)
{
    int i;
    for (i = 0; i < cm->count; i++) {
        if (strncmp(cm->concepts[i].name, concept, 63) == 0)  /* 63-char name limit */
            return i;
    }
    return -1;                                    /* Not found */
}

/*
 * ao_mass_observe -- Record a D2 observation for a named concept.
 *
 * WHAT: Accumulates mass, updates EMA d2_mean, increments observation
 *       count, and updates vortex fingerprint for the given concept.
 *
 * HOW:
 *   1. Compute Euclidean magnitude of D2 vector:
 *      mag = sqrt(d2[0]^2 + d2[1]^2 + d2[2]^2 + d2[3]^2 + d2[4]^2)
 *      (L2 norm, not L1. L2 used here because mass should be rotationally
 *      invariant -- the total curvature regardless of direction.)
 *
 *   2. Find or create the concept entry:
 *      - Look up by name. If not found and count < 256, create new.
 *      - If array is full, return 0.0 (silent failure).
 *
 *   3. Accumulate mass: mass += mag.
 *      Mass is the integral of curvature magnitude over all observations.
 *
 *   4. EMA update for d2_mean:
 *      - First observation: d2_mean = d2 (initialize directly).
 *      - Subsequent: d2_mean = 0.9 * d2_mean + 0.1 * d2.
 *
 *      The 0.9/0.1 EMA coefficients:
 *        0.9 = retention factor. 90% of old mean is kept.
 *        0.1 = learning rate. 10% of new observation is blended in.
 *        Effective window: ~10 observations (1/0.1) to shift the mean
 *        significantly. This makes d2_mean a stable, slowly-evolving
 *        signature of the concept's curvature character.
 *
 *   5. Increment observations count.
 *
 *   6. Update vortex fingerprint if operators are provided.
 *
 * WHY:  This is how AO builds knowledge about concepts. Each time AO
 *       studies text about a concept, the D2 curvature is measured and
 *       accumulated. Over time, heavy concepts (high mass) represent
 *       deep knowledge, and d2_mean captures the curvature signature
 *       (what this concept "feels like" in 5D force space).
 *
 * Returns: the concept's total mass after this observation.
 *          Returns 0.0 if the concept array is full and a new concept
 *          could not be created.
 */
float ao_mass_observe(AO_ConceptMass* cm, const char* concept,
                      const float d2[5], const int* ops, int n_ops)
{
    int idx;
    AO_Concept* c;
    float mag;
    int i;

    /* Compute Euclidean magnitude (L2 norm) of D2 vector */
    mag = 0.0f;
    for (i = 0; i < 5; i++)
        mag += d2[i] * d2[i];                    /* Sum of squares */
    mag = sqrtf(mag);                             /* Square root for L2 norm */

    /* Find or create concept entry */
    idx = ao_mass_find(cm, concept);
    if (idx < 0) {
        if (cm->count >= AO_MAX_CONCEPTS)         /* AO_MAX_CONCEPTS = 256 */
            return 0.0f;                          /* Array full: cannot create new */
        idx = cm->count++;
        c = &cm->concepts[idx];
        memset(c, 0, sizeof(*c));
        strncpy(c->name, concept, 63);            /* 63-char name limit */
        c->name[63] = '\0';                       /* Ensure NUL termination */
    }

    c = &cm->concepts[idx];

    /* Accumulate mass: integral of D2 magnitude over all observations */
    c->mass += mag;

    /* EMA update for d2_mean: exponential moving average of D2 vectors.
     * Alpha = 0.1 (learning rate), Beta = 0.9 (retention).
     * d2_mean tracks the average curvature direction for this concept. */
    if (c->observations == 0) {
        /* First observation: initialize d2_mean directly (no blending) */
        for (i = 0; i < 5; i++)
            c->d2_mean[i] = d2[i];
    } else {
        /* Subsequent: EMA blend -- 90% old + 10% new */
        for (i = 0; i < 5; i++)
            c->d2_mean[i] = 0.9f * c->d2_mean[i]   /* 0.9 = retention (old stays) */
                           + 0.1f * d2[i];           /* 0.1 = learning (new blends in) */
    }

    c->observations++;

    /* Update vortex fingerprint (topological signature of operator sequences) */
    if (ops && n_ops > 0)
        ao_vortex_fingerprint(ops, n_ops, &c->vortex);

    return c->mass;
}

/*
 * ao_mass_get -- Query the accumulated mass of a named concept.
 *
 * WHAT: Returns the total mass for the given concept name.
 * HOW:  Linear scan to find the concept, then return its mass field.
 * WHY:  Simple query for how much AO has studied a topic.
 *
 * Returns: mass (float >= 0). Returns 0.0 if concept not found.
 */
float ao_mass_get(const AO_ConceptMass* cm, const char* concept)
{
    int idx = ao_mass_find(cm, concept);
    if (idx < 0) return 0.0f;                    /* Unknown concept: zero mass */
    return cm->concepts[idx].mass;
}

/*
 * ao_mass_gravity -- Compute gravitational pull of a concept on AO.
 *
 * WHAT: Returns gravity = mass * coherence * cos_similarity.
 *       Models how strongly a familiar concept "pulls" AO toward it.
 *
 * HOW:
 *   1. Find the concept by name. If not found, return 0.
 *   2. Compute cosine similarity between current_d2 and the concept's
 *      d2_mean (average curvature direction):
 *        cos_sim = dot(current_d2, d2_mean) / (|current_d2| * |d2_mean|)
 *      Using standard dot product and L2 norms.
 *   3. Gravity = mass * coherence * cos_sim.
 *
 * WHY:  This is a physics-inspired attraction model:
 *
 *       - MASS: How much AO knows about this concept. Heavy concepts
 *         have been studied extensively and have strong pull.
 *
 *       - COHERENCE: How confident AO is right now. When coherence is
 *         high, gravity is strong (confident pull). When coherence is
 *         low, gravity is weak (uncertain, don't commit).
 *
 *       - COS_SIMILARITY: How aligned the current curvature is with
 *         the concept's signature direction. +1 = perfectly aligned
 *         (strong pull), 0 = orthogonal (no pull), -1 = opposite
 *         (repulsion -- current input is anti-correlated with concept).
 *
 *       High gravity means: "I deeply know this concept, I'm currently
 *       confident, and what I'm seeing right now LOOKS like this concept."
 *       This guides AO toward familiar, well-understood territory.
 *
 * Parameters:
 *   cm         -- concept mass tracker
 *   concept    -- name of the concept to check
 *   coherence  -- current coherence level (from coherence window)
 *   current_d2 -- current D2 vector (from the D2 pipeline)
 *
 * Returns: gravity (float). Can be negative if cos_sim is negative.
 *          Returns 0.0 if concept not found or vectors are zero.
 */
float ao_mass_gravity(const AO_ConceptMass* cm, const char* concept,
                      float coherence, const float current_d2[5])
{
    int idx;
    const AO_Concept* c;
    float dot = 0.0f;
    float mag_mean = 0.0f;
    float mag_curr = 0.0f;
    float cos_sim;
    int i;

    idx = ao_mass_find(cm, concept);
    if (idx < 0) return 0.0f;                    /* Unknown concept: no gravity */

    c = &cm->concepts[idx];

    /* Cosine similarity between current_d2 and d2_mean.
     * cos_sim = dot(a, b) / (|a| * |b|)
     * where a = current_d2, b = concept's average curvature direction. */
    for (i = 0; i < 5; i++) {
        dot      += current_d2[i] * c->d2_mean[i];    /* Dot product numerator */
        mag_mean += c->d2_mean[i] * c->d2_mean[i];    /* |d2_mean|^2 */
        mag_curr += current_d2[i] * current_d2[i];    /* |current_d2|^2 */
    }

    mag_mean = sqrtf(mag_mean);                   /* |d2_mean| (L2 norm) */
    mag_curr = sqrtf(mag_curr);                   /* |current_d2| (L2 norm) */

    if (mag_mean < 1e-12f || mag_curr < 1e-12f)  /* 1e-12 = near-zero guard to avoid /0 */
        cos_sim = 0.0f;                           /* Zero vectors: no similarity */
    else
        cos_sim = dot / (mag_mean * mag_curr);    /* Cosine similarity in [-1, +1] */

    /* Gravity = mass * coherence * cos_similarity
     * Heavy + confident + aligned = strong pull. */
    return c->mass * coherence * cos_sim;
}

/* ══════════════════════════════════════════════════════════════════════
 * Section 7: SPECTROMETER (parallel D1+D2 text measurement)
 *
 * The spectrometer feeds every a-z character in a text through BOTH
 * the D1 (velocity) and D2 (curvature) pipelines simultaneously.
 * It produces:
 *   - d1_hist[10]: histogram of D1 operators (how often each op appears)
 *   - d2_hist[10]: histogram of D2 operators
 *   - coherence: HARMONY fraction from a coherence window over D2 ops
 *   - shell: TSML shell selection (22/44/72) based on coherence
 *   - band: color band (RED/YELLOW/GREEN) based on coherence
 *   - d2_magnitude_avg: average L1 magnitude of D2 vectors
 *   - d1_d2_agreement: percentage of positions where D1 and D2 classify
 *     to the same operator (velocity agrees with curvature)
 *
 * The spectrometer is a complete text-level measurement tool. Feed it
 * any string and get back a comprehensive operator profile.
 * ══════════════════════════════════════════════════════════════════════ */

/*
 * ao_measure_text -- Measure a text string through parallel D1+D2 pipelines.
 *
 * WHAT: Feeds every a-z letter through both D1 and D2 pipelines, collecting
 *       operator histograms, coherence, and D1-D2 agreement statistics.
 *
 * HOW:
 *   1. Initialize a D2 pipeline, a D1 pipeline, and a coherence window.
 *   2. For each character in the text:
 *      a. Uppercase -> lowercase. Skip non-alpha characters.
 *      b. Convert to index (0-25) and feed to both D1 and D2 pipelines.
 *      c. If both pipelines are valid (D1: >= 2 symbols, D2: >= 3 symbols):
 *         - Classify D1 and D2 operators.
 *         - Increment d1_hist[d1_op] and d2_hist[d2_op].
 *         - Feed D2 operator into coherence window.
 *         - Accumulate D2 L1 magnitude.
 *         - Count D1-D2 agreements (same operator from both pipelines).
 *   3. Finalize:
 *      - coherence = harmony_count / window_count
 *      - shell = 22/44/72 based on coherence thresholds
 *      - band = RED/YELLOW/GREEN
 *      - d1_d2_agreement = (agreements / d2_total) * 100 (percentage)
 *      - d2_magnitude_avg = total_magnitude / d2_total
 *
 * WHY:  The spectrometer gives a complete picture of a text's operator
 *       profile. D1 and D2 measure different things (velocity vs curvature),
 *       so their agreement tells you how self-consistent the text is.
 *       High agreement = the text's direction and curvature align (stable).
 *       Low agreement = direction and curvature diverge (turbulent).
 *
 *       Coherence (HARMONY fraction) tells you how harmonious the
 *       curvature pattern is. D2 magnitude tells you how "sharp" the
 *       curvature is on average. Together these give a multi-dimensional
 *       fingerprint of the text's force structure.
 */
void ao_measure_text(const char* text, AO_Measurement* out)
{
    AO_D2Pipeline pipe;
    AO_D1Pipeline d1_pipe;
    AO_CoherenceWindow window;
    int i, idx;
    int agreements = 0;                           /* Count of D1==D2 matches */

    memset(out, 0, sizeof(*out));
    ao_d2_init(&pipe);
    ao_d1_init(&d1_pipe);
    ao_cw_init(&window);

    for (i = 0; text[i]; i++) {
        char ch = text[i];
        if (ch >= 'A' && ch <= 'Z') ch = ch - 'A' + 'a';  /* To lowercase */
        if (ch < 'a' || ch > 'z') continue;      /* Skip non-alpha */
        idx = ch - 'a';                           /* Convert to 0-25 index */

        ao_d1_feed(&d1_pipe, idx);                /* Feed into D1 pipeline */
        ao_d2_feed(&pipe, idx);                   /* Feed into D2 pipeline */
        out->total_symbols++;

        /* Both pipelines valid: D2 needs >= 3 symbols, D1 needs >= 2 */
        if (pipe.d2_valid && d1_pipe.valid) {
            int d1_op = ao_d1_classify(&d1_pipe);     /* Classify D1 (velocity) */
            int d2_op = ao_d2_classify_d2(&pipe);     /* Classify D2 (curvature) */
            out->d1_hist[d1_op]++;                    /* Tally D1 operator */
            out->d2_hist[d2_op]++;                    /* Tally D2 operator */
            ao_cw_observe(&window, d2_op);            /* Feed D2 op into coherence window */
            out->d2_magnitude_avg += ao_d2_magnitude(&pipe);  /* Accumulate magnitude */
            out->d2_total++;

            if (d1_op == d2_op) agreements++;     /* D1 and D2 agree on operator */
        }
    }

    /* Finalize aggregated measurements */
    out->coherence = ao_cw_coherence(&window);
    out->shell = ao_cw_shell(&window);            /* 22/44/72 based on coherence */
    out->band = ao_cw_band(&window);              /* RED(0)/YELLOW(1)/GREEN(2) */
    out->d1_d2_agreement = out->d2_total > 0
        ? (float)agreements / (float)out->d2_total * 100.0f   /* Percentage */
        : 0.0f;
    out->d2_magnitude_avg = out->d2_total > 0
        ? out->d2_magnitude_avg / (float)out->d2_total        /* Average */
        : 0.0f;
}

/* ══════════════════════════════════════════════════════════════════════
 * Section 8: SHANNON ENTROPY of an operator histogram
 *
 * Shannon entropy H = -sum(p_i * log2(p_i)) measures the uncertainty
 * or information content of a probability distribution.
 *
 *   H = 0 bits:          Only one operator has nonzero count (perfectly
 *                         predictable, no uncertainty).
 *
 *   H = log2(10) ~ 3.32: All 10 operators equally likely (maximum
 *                         uncertainty, completely unpredictable).
 *
 *   Low H:  The distribution is concentrated on a few operators.
 *           The text is dominated by specific curvature patterns.
 *
 *   High H: The distribution is spread across many operators.
 *           The text has diverse curvature patterns.
 *
 * Convention: 0 * log2(0) = 0 (the limit as p->0 of p*log2(p) is 0).
 * We handle this by skipping zero-count bins.
 * ══════════════════════════════════════════════════════════════════════ */

/*
 * ao_entropy -- Compute Shannon entropy of a 10-bin operator histogram.
 *
 * WHAT: Returns H = -sum(p_i * log2(p_i)) for the given histogram.
 * HOW:
 *   1. Sum all bins to get total count.
 *   2. If total == 0, return 0.0 (no data).
 *   3. For each nonzero bin: p = hist[i] / total, accumulate -p * log2(p).
 * WHY:  General-purpose entropy function used by the spectrometer,
 *       diagnostics, and any code that needs to measure the spread
 *       of an operator distribution.
 *
 * Parameters:
 *   hist -- array of AO_NUM_OPS (10) integer counts.
 *
 * Returns: Shannon entropy in bits (float). Range [0, log2(10) ~ 3.32].
 *          Returns 0.0 if all counts are zero.
 */
float ao_entropy(const int hist[AO_NUM_OPS])
{
    int total = 0, i;
    float h = 0.0f;

    /* Sum all bins to get total count */
    for (i = 0; i < AO_NUM_OPS; i++)             /* AO_NUM_OPS = 10 */
        total += hist[i];

    if (total == 0) return 0.0f;                  /* No data: zero entropy */

    /* Shannon entropy: H = -sum(p * log2(p)) */
    for (i = 0; i < AO_NUM_OPS; i++) {
        if (hist[i] > 0) {                        /* Skip zero bins (0*log2(0) = 0) */
            float p = (float)hist[i] / (float)total;
            h -= p * log2f(p);                    /* -p * log2(p), accumulated */
        }
    }

    return h;
}
