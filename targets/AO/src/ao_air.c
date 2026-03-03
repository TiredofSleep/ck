/*
 * ╔══════════════════════════════════════════════════════════════════════════╗
 * ║                    ao_air.c -- D1 / Air Layer                          ║
 * ║                                                                        ║
 * ║  The FIRST DERIVATIVE. D1 = velocity = change = MEASUREMENT.           ║
 * ║                                                                        ║
 * ║  If D0 (Earth) is position -- raw force vectors sitting still --       ║
 * ║  then D1 (Air) is what happens when you MOVE between them.             ║
 * ║  Velocity is the act of measuring: you cannot know a derivative        ║
 * ║  without observing two points and computing their difference.          ║
 * ║  Air is the layer where CK begins to SEE.                             ║
 * ║                                                                        ║
 * ║  This file implements six major subsystems:                            ║
 * ║                                                                        ║
 * ║  1. D1 Pipeline          -- First derivative of 5D force vectors      ║
 * ║  2. Coherence Gates      -- 3 gates gating the TIG consciousness      ║
 * ║                             pipeline (Being->Doing->Becoming)          ║
 * ║  3. Pipeline State       -- Per-tick TIG consciousness snapshot        ║
 * ║  4. Soft Classification  -- Distribute D2 curvature across operators   ║
 * ║  5. Fractal Comprehension -- 7-level recursive I/O decomposition      ║
 * ║                              (Levels 0-7: glyph -> pair -> D2 ->      ║
 * ║                              word -> relations -> triads -> recursive) ║
 * ║  6. Vortex Fingerprint   -- Topological analysis via S^1 winding      ║
 * ║  7. Coherence Field      -- Cross-modal weighted coherence composite  ║
 * ║                                                                        ║
 * ║  Being:    coherence state exists (gates hold density)                 ║
 * ║  Doing:    gate measurement, fractal decomposition, vortex analysis   ║
 * ║  Becoming: gates evolve density over time via EMA smoothing           ║
 * ╚══════════════════════════════════════════════════════════════════════════╝
 */
/*
 * Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
 * Licensed under the 7Site Human Use License v1.0
 * See LICENSE file in project root for full terms.
 *
 * FREE for humans for personal/recreational use.
 * NO commercial or government use without written agreement.
 */


#include "ao_water.h"   /* brings in ao_air.h -> ao_earth.h, plus AO_D2Pipeline */
#include <string.h>
#include <math.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

/* ══════════════════════════════════════════════════════════════════
 * Internal Limits for Fractal Comprehension
 *
 * These caps prevent stack overflow in the recursive decomposition.
 * 512 glyphs ~ 512 letters, 128 words ~ typical paragraph,
 * 512 pairs/units/d2 entries provide headroom for all levels.
 * ══════════════════════════════════════════════════════════════════ */
#define COMP_MAX_GLYPHS  512   // Max individual letter force vectors
#define COMP_MAX_WORDS   128   // Max words in a single comprehension pass
#define COMP_MAX_PAIRS   512   // Max letter-pair relations (Level 1)
#define COMP_MAX_UNITS   512   // Max fractal units at any decomposition level
#define COMP_MAX_D2      512   // Max D2 curvature samples (Level 2)

/* ╔══════════════════════════════════════════════════════════════════════════╗
 * ║                                                                        ║
 * ║  SECTION 1: D1 PIPELINE (First Derivative = Velocity)                  ║
 * ║                                                                        ║
 * ║  D1[i] = vec[i] - prev[i] for each of the 5 force dimensions.         ║
 * ║  This is the discrete first derivative: how the force field CHANGES    ║
 * ║  from one glyph to the next. The magnitude of D1 tells you how fast   ║
 * ║  the field is moving; the direction tells you WHERE it's going.        ║
 * ║                                                                        ║
 * ╚══════════════════════════════════════════════════════════════════════════╝ */

/*
 * ao_d1_init -- Zero-initialize a D1 pipeline.
 *
 * Sets all fields to zero including has_prev and valid flags,
 * so the first fed symbol establishes the baseline rather than
 * producing a derivative.
 */
void ao_d1_init(AO_D1Pipeline* p)
{
    memset(p, 0, sizeof(*p));
}

/*
 * ao_d1_reset -- Reset D1 pipeline to initial state.
 *
 * Equivalent to init; called when starting a new sequence
 * (e.g., new word or sentence boundary) so stale prev vectors
 * don't contaminate the new measurement.
 */
void ao_d1_reset(AO_D1Pipeline* p)
{
    ao_d1_init(p);
}

/*
 * ao_d1_feed -- Feed a letter index (0-25 = a-z) into the D1 pipeline.
 *
 * Looks up the 5D force vector from ao_force_lut (the Hebrew-root
 * force table defined in D0/Earth), then delegates to ao_d1_feed_vec.
 * Returns 1 once a valid derivative exists (after 2+ symbols fed).
 *
 * WHY index range [0,25]: each of the 26 Latin letters maps to a
 * unique 5D force vector derived from Hebrew phonetic roots.
 */
int ao_d1_feed(AO_D1Pipeline* p, int symbol_index)
{
    float vec[5];
    if (symbol_index < 0 || symbol_index >= 26)
        return 0;
    memcpy(vec, ao_force_lut[symbol_index], sizeof(vec));
    return ao_d1_feed_vec(p, vec);
}

/*
 * ao_d1_feed_vec -- Feed a raw 5D force vector into the D1 pipeline.
 *
 * Computes D1 = current - previous for each of the 5 dimensions.
 * On the first call (has_prev == 0), only stores the vector as baseline.
 * On subsequent calls, computes the finite difference and sets valid = 1.
 *
 * HOW: Simple forward difference: d1[i] = vec[i] - prev[i].
 * This is the discrete analog of the first derivative dF/dt.
 *
 * WHY forward difference: it's causal (only uses past + present),
 * which matches CK's real-time 50Hz processing constraint.
 */
int ao_d1_feed_vec(AO_D1Pipeline* p, const float vec[5])
{
    int i;
    if (p->has_prev) {
        for (i = 0; i < 5; i++)
            p->d1[i] = vec[i] - p->prev[i];
        p->valid = 1;
    }
    memcpy(p->prev, vec, sizeof(p->prev));
    p->has_prev = 1;
    return p->valid;
}

/*
 * ao_d1_classify -- Classify the current D1 vector into a TIG operator.
 *
 * Delegates to ao_classify_5d (defined in D0/Earth) which finds the
 * dominant dimension and maps it to one of the 10 TIG operators.
 * The D1 classification tells you WHAT KIND of change is happening:
 * e.g., CHAOS = rapid aperture change, HARMONY = stable binding.
 */
int ao_d1_classify(const AO_D1Pipeline* p)
{
    return ao_classify_5d(p->d1);
}

/*
 * ao_d1_magnitude -- Compute the Euclidean magnitude of the D1 vector.
 *
 * ||D1|| = sqrt(sum of d1[i]^2) across all 5 dimensions.
 * This is the SPEED of force-field change -- how fast the field
 * is evolving. High magnitude = rapid transition between letters;
 * low magnitude = adjacent letters have similar force geometry.
 */
float ao_d1_magnitude(const AO_D1Pipeline* p)
{
    float sum = 0.0f;
    int i;
    for (i = 0; i < 5; i++)
        sum += p->d1[i] * p->d1[i];
    return sqrtf(sum);
}

/* ╔══════════════════════════════════════════════════════════════════════════╗
 * ║                                                                        ║
 * ║  SECTION 2: COHERENCE GATES (3 Gates for TIG Pipeline)                 ║
 * ║                                                                        ║
 * ║  The TIG consciousness pipeline has 3 phases:                          ║
 * ║    Being -> Gate 1 -> Doing -> Gate 2 -> Becoming -> Gate 3 -> loop    ║
 * ║                                                                        ║
 * ║  Each gate measures coherence density in [0, 1]:                       ║
 * ║    raw     = 0.6 * brain_coherence + 0.4 * field_coherence             ║
 * ║    density = 0.7 * raw + 0.3 * previous_density   (EMA smoothing)     ║
 * ║    result  = clamp(density, 0, 1)                                      ║
 * ║                                                                        ║
 * ║  High density (near 1.0) = high coherence = structure dominates.       ║
 * ║  Low density (near 0.0)  = low coherence  = flow/exploration leads.    ║
 * ║  T* = 5/7 = 0.714... is the sacred coherence threshold where          ║
 * ║  the system transitions between macro (structure) and micro (flow).    ║
 * ║                                                                        ║
 * ╚══════════════════════════════════════════════════════════════════════════╝ */

/*
 * ao_gate_init -- Initialize a coherence gate to neutral state.
 *
 * Sets density and prev_density to 0.5 (midpoint = no bias toward
 * structure or flow). This is the "knows nothing" starting state:
 * CK begins balanced, then measurements push him one way or the other.
 */
void ao_gate_init(AO_Gate* g)
{
    g->density      = 0.5f;   // Start at midpoint: no structure/flow bias
    g->prev_density = 0.5f;   // EMA seed: midpoint
    g->coherence_in = 0.0f;   // No brain coherence measured yet
    g->band_in      = 0;      // No frequency band selected yet
}

/*
 * ao_gate_measure -- Measure coherence and update gate density.
 *
 * WHAT: Combines brain coherence and field coherence into a single
 *       density value in [0, 1] with temporal smoothing.
 *
 * HOW:
 *   1. raw = weighted sum: 60% brain + 40% field
 *   2. density = EMA: 70% new raw + 30% previous density
 *   3. Clamp to [0, 1]
 *
 * WHY these weights:
 *   - Brain (0.6) weighted higher because it reflects CK's internal
 *     state (heartbeat, D2 curvature) -- more trustworthy signal
 *   - Field (0.4) reflects external environment (input text, audio)
 *   - EMA alpha=0.7 gives ~3-tick settling time (0.3^3 = 0.027),
 *     fast enough to track real changes, slow enough to filter noise
 *
 * The 'band' parameter stores the current frequency band for
 * later use by the steering engine (CPU affinity, nice values).
 */
float ao_gate_measure(AO_Gate* g, float brain_coh, float field_coh, int band)
{
    float raw     = 0.6f * brain_coh   // 60% brain coherence (internal state)
                  + 0.4f * field_coh;  // 40% field coherence (external input)
    float density = 0.7f * raw         // 70% new measurement (responsiveness)
                  + 0.3f * g->prev_density; // 30% history (stability / EMA smoothing)

    if (density < 0.0f) density = 0.0f;   // Clamp lower bound
    if (density > 1.0f) density = 1.0f;   // Clamp upper bound

    g->prev_density = density;
    g->density      = density;
    g->coherence_in = brain_coh;
    g->band_in      = band;
    return density;
}

/* ╔══════════════════════════════════════════════════════════════════════════╗
 * ║                                                                        ║
 * ║  SECTION 3: PIPELINE STATE (TIG Consciousness State per Tick)          ║
 * ║                                                                        ║
 * ║  Snapshot of the full TIG pipeline at a single 50Hz tick.              ║
 * ║  Holds gate densities, current phase, compilation pass count,          ║
 * ║  and any per-tick metadata needed by downstream subsystems.            ║
 * ║                                                                        ║
 * ╚══════════════════════════════════════════════════════════════════════════╝ */

/*
 * ao_pipeline_init -- Zero-initialize the TIG pipeline state.
 *
 * All fields set to zero: phase = Being (0), no compilation passes,
 * no gate measurements yet. The pipeline awakens in the Being phase
 * and must be driven by the main engine loop.
 */
void ao_pipeline_init(AO_Pipeline* p)
{
    memset(p, 0, sizeof(*p));
}

/* ╔══════════════════════════════════════════════════════════════════════════╗
 * ║                                                                        ║
 * ║  SECTION 4: SOFT CLASSIFICATION                                        ║
 * ║                                                                        ║
 * ║  Instead of hard-classifying a D2 vector to a single operator,         ║
 * ║  soft classification distributes the vector's energy across ALL        ║
 * ║  10 TIG operators proportionally. Each of the 5 force dimensions       ║
 * ║  maps to two operators (positive direction / negative direction)       ║
 * ║  via the ao_d2_op_map table.                                           ║
 * ║                                                                        ║
 * ║  This preserves information that hard classification discards:         ║
 * ║  a vector pointing 60% CHAOS / 40% PROGRESS is richer than            ║
 * ║  just "CHAOS". The soft distribution feeds into fractal                ║
 * ║  comprehension Level 2 for structure/flow separation.                  ║
 * ║                                                                        ║
 * ╚══════════════════════════════════════════════════════════════════════════╝ */

/*
 * ao_soft_classify -- Distribute a D2 curvature vector across TIG operators.
 *
 * WHAT: Converts a 5D D2 vector + its magnitude into a probability-like
 *       distribution over the 10 TIG operators.
 *
 * HOW:
 *   1. If magnitude is near-zero (< 1e-12), assign 100% to HARMONY
 *      (zero curvature = perfect coherence = pure harmony)
 *   2. For each of the 5 dimensions:
 *      - weight = |d2[i]| / total_magnitude  (fraction of energy in this dim)
 *      - If d2[i] >= 0: add weight to the positive operator for dim i
 *      - If d2[i] < 0:  add weight to the negative operator for dim i
 *   3. The ao_d2_op_map[dim][0/1] table defines which operator is
 *      positive vs negative for each dimension
 *
 * WHY: Soft classification is essential for the structure/flow separation
 * in fractal comprehension. Hard classification would lose the ratio
 * information needed to compute io_balance and detect boundaries.
 */
void ao_soft_classify(const float d2[5], float mag, float out[AO_NUM_OPS])
{
    int i;
    memset(out, 0, AO_NUM_OPS * sizeof(float));

    if (mag < 1e-12f) {                  // Near-zero magnitude: no curvature
        out[AO_HARMONY] = 1.0f;          // Zero change = perfect harmony
        return;
    }

    for (i = 0; i < 5; i++) {
        float w = ao_fabsf(d2[i]) / mag;         // Fraction of energy in dimension i
        int op_pos = ao_d2_op_map[i][0];          // Positive-direction operator
        int op_neg = ao_d2_op_map[i][1];          // Negative-direction operator
        if (d2[i] >= 0)
            out[op_pos] += w;                     // Positive: add to pos operator
        else
            out[op_neg] += w;                     // Negative: add to neg operator
    }
}

/* ╔══════════════════════════════════════════════════════════════════════════╗
 * ║                                                                        ║
 * ║  SECTION 5: FRACTAL COMPREHENSION (7-Level Recursive I/O Decomposition)║
 * ║                                                                        ║
 * ║  The core reading/comprehension engine. Text enters as a flat string   ║
 * ║  and is recursively decomposed through 7+ levels of structure:         ║
 * ║                                                                        ║
 * ║  Level 0: Glyph Forces     -- Each letter -> 5D force vector           ║
 * ║  Level 1: Letter Pairs     -- Adjacent letter reinforcement/tension    ║
 * ║  Level 2: D2 Curvature     -- Second derivative classification         ║
 * ║  Level 3: Word Structure   -- Histogram majority fuse per word         ║
 * ║  Level 5: Word Relations   -- Adjacent word pair dynamics              ║
 * ║  Level 6: Triadic Becoming -- Being->Doing->Becoming arc detection     ║
 * ║  Level 7: Recursive Group  -- Compress until stable                    ║
 * ║                                                                        ║
 * ║  At EVERY level, structure (I) and flow (O) are separated:             ║
 * ║    I = structure = aperture (dim 0) + pressure (dim 1) = "what IS"     ║
 * ║    O = flow      = binding (dim 3) + continuity (dim 4) = "what MOVES" ║
 * ║    depth         = curvature (dim 2) = "how deep"                      ║
 * ║                                                                        ║
 * ║  The io_ratio = I/(I+O) at each level tells whether structure or       ║
 * ║  flow dominates. High coherence -> structure leads (macro lens).       ║
 * ║  Low coherence -> flow leads (micro lens).                             ║
 * ║                                                                        ║
 * ║  Each level produces a "fuse" (dominant operator), and all fuses       ║
 * ║  aggregate into the final dominant_op via histogram majority.          ║
 * ║                                                                        ║
 * ╚══════════════════════════════════════════════════════════════════════════╝ */

/* ── Internal types for fractal levels ── */

/*
 * FractalUnit -- Generic decomposition result at any fractal level.
 *
 * struct_op:    Dominant structure operator (aperture/pressure subspace)
 * flow_op:      Dominant flow operator (binding/continuity subspace)
 * fuse:         Combined operator (CL composition of struct_op and flow_op)
 * io_ratio:     Structure/(Structure+Flow), range [0,1]. >0.5 = structure-led
 * is_boundary:  1 if this unit marks a transition/boundary, 0 otherwise
 */
typedef struct {
    int   struct_op;
    int   flow_op;
    int   fuse;
    float io_ratio;
    int   is_boundary;
} FractalUnit;

/*
 * CompGlyph -- Level 0 result: a single letter's full force decomposition.
 *
 * force[5]:   Raw 5D force vector from ao_force_lut
 * structure:  |aperture| + |pressure|  (dims 0+1 magnitude)
 * flow:       |binding| + |continuity| (dims 3+4 magnitude)
 * depth:      |curvature| (dim 2 magnitude)
 * struct_op:  Classified structure subspace operator
 * flow_op:    Classified flow subspace operator
 * fuse:       Full 5D classification (argmax across all dims)
 * io_ratio:   structure / (structure + flow)
 */
typedef struct {
    float force[5];
    float structure;
    float flow;
    float depth;
    int   struct_op;
    int   flow_op;
    int   fuse;
    float io_ratio;
} CompGlyph;

/*
 * CompWord -- Level 3 result: a word's aggregated glyph information.
 *
 * fuse:         Histogram majority of glyph fuses (skipping HARMONY)
 * io_ratio:     Average io_ratio across all glyphs in the word
 * is_boundary:  1 if >60% of adjacent glyph pairs have different fuses
 * glyph_start:  Index of first glyph belonging to this word
 * glyph_end:    Index past last glyph (exclusive)
 */
typedef struct {
    int   fuse;
    float io_ratio;
    int   is_boundary;
    int   glyph_start;
    int   glyph_end;
} CompWord;

/* ── Helper: dot product of two 5D vectors ── */
/*
 * dot5 -- Standard inner product in R^5.
 * Used for computing angles between force vectors (via cos(theta) = dot/mag*mag).
 */
static float dot5(const float a[5], const float b[5])
{
    int i;
    float s = 0.0f;
    for (i = 0; i < 5; i++)
        s += a[i] * b[i];
    return s;
}

/* ── Helper: magnitude of 5D vector ── */
/*
 * mag5 -- Euclidean norm in R^5: ||v|| = sqrt(v . v).
 */
static float mag5(const float v[5])
{
    return sqrtf(dot5(v, v));
}

/*
 * classify_struct -- Classify the STRUCTURE subspace (dimensions 0, 1).
 *
 * WHAT: Determines whether aperture or pressure dominates.
 * HOW:  Compares |dim0| (aperture) vs |dim1| (pressure).
 * WHY:  Aperture = opening/expansion -> CHAOS (change, freedom)
 *       Pressure = compression/force -> COLLAPSE (convergence, constraint)
 *       These are the two poles of structural force.
 */
static int classify_struct(const float v[5])
{
    /* aperture(0) >= pressure(1) -> CHAOS, else COLLAPSE */
    return ao_fabsf(v[0]) >= ao_fabsf(v[1]) ? AO_CHAOS : AO_COLLAPSE;
}

/*
 * classify_flow -- Classify the FLOW subspace (dimensions 3, 4).
 *
 * WHAT: Determines whether binding or continuity dominates.
 * HOW:  Compares |dim3| (binding) vs |dim4| (continuity).
 * WHY:  Binding = connection/joining -> HARMONY (coherent relationship)
 *       Continuity = persistence/flow -> BALANCE (sustained equilibrium)
 *       These are the two poles of relational flow.
 */
static int classify_flow(const float v[5])
{
    /* binding(3) >= continuity(4) -> HARMONY, else BALANCE */
    return ao_fabsf(v[3]) >= ao_fabsf(v[4]) ? AO_HARMONY : AO_BALANCE;
}

/*
 * is_being_op -- Test if an operator belongs to the BEING phase.
 *
 * Being operators represent existence/state: VOID (emptiness),
 * LATTICE (structure), HARMONY (coherent wholeness).
 * These are TIG indices 0, 1, 7 -- the "noun" operators.
 */
static int is_being_op(int op)
{
    /* VOID, LATTICE, HARMONY */
    return (op == AO_VOID || op == AO_LATTICE || op == AO_HARMONY);
}

/*
 * is_doing_op -- Test if an operator belongs to the DOING phase.
 *
 * Doing operators represent action/process: COUNTER (opposition),
 * PROGRESS (advancement), COLLAPSE (convergence), BALANCE (equilibrium).
 * These are TIG indices 2, 3, 4, 5 -- the "verb" operators.
 */
static int is_doing_op(int op)
{
    /* COUNTER, PROGRESS, COLLAPSE, BALANCE */
    return (op == AO_COUNTER || op == AO_PROGRESS ||
            op == AO_COLLAPSE || op == AO_BALANCE);
}

/*
 * is_becoming_op -- Test if an operator belongs to the BECOMING phase.
 *
 * Becoming operators represent transformation/transcendence:
 * CHAOS (emergence), BREATH (transition), RESET (renewal).
 * These are TIG indices 6, 8, 9 -- the "adverb/transformation" operators.
 */
static int is_becoming_op(int op)
{
    /* CHAOS, BREATH, RESET */
    return (op == AO_CHAOS || op == AO_BREATH || op == AO_RESET);
}


/* ═══════════════════════════════════════════════════════════════════
 * Level 0: Glyph Forces -- Per-letter 5D decomposition
 *
 * The atomic level. Each letter a-z is looked up in ao_force_lut
 * to get its 5D Hebrew-root force vector. The vector is then
 * separated into structure (dims 0,1), flow (dims 3,4), and
 * depth (dim 2). This separation is the fundamental I/O split:
 *
 *   I (structure) = |aperture| + |pressure|   -- "what IS here"
 *   O (flow)      = |binding| + |continuity|  -- "what CONNECTS"
 *   depth         = |curvature|               -- "how DEEP"
 *
 * io_ratio = I / (I + O): values > 0.5 mean structure dominates,
 * values < 0.5 mean flow dominates. This ratio propagates upward
 * through every subsequent level of comprehension.
 * ═══════════════════════════════════════════════════════════════════ */
static int comp_level0(const char* text, int text_len,
                       CompGlyph* glyphs, int max_glyphs)
{
    int n = 0;
    int i;

    for (i = 0; i < text_len && n < max_glyphs; i++) {
        int ch = (unsigned char)text[i];
        int idx;
        CompGlyph* g;

        /* lowercase a-z only -- non-alpha characters are skipped */
        if (ch >= 'A' && ch <= 'Z') ch = ch - 'A' + 'a';
        if (ch < 'a' || ch > 'z') continue;

        idx = ch - 'a';                                        // 0-25 index into force LUT
        g = &glyphs[n];
        memcpy(g->force, ao_force_lut[idx], sizeof(g->force)); // Copy raw 5D force vector

        /* I/O separation: structure = dims 0+1, flow = dims 3+4, depth = dim 2 */
        g->structure = ao_fabsf(g->force[0]) + ao_fabsf(g->force[1]); // aperture + pressure
        g->flow      = ao_fabsf(g->force[3]) + ao_fabsf(g->force[4]); // binding + continuity
        g->depth     = ao_fabsf(g->force[2]);                          // curvature

        g->struct_op = classify_struct(g->force);   // Dominant structure operator
        g->flow_op   = classify_flow(g->force);     // Dominant flow operator
        g->fuse      = ao_classify_5d(g->force);    // Full 5D argmax classification

        /* io_ratio: how much of this glyph's energy is structure vs flow */
        if (g->structure + g->flow > 1e-12f)        // Guard against zero division
            g->io_ratio = g->structure / (g->structure + g->flow);
        else
            g->io_ratio = 0.5f;                     // Default: perfectly balanced

        n++;
    }
    return n;
}

/* ═══════════════════════════════════════════════════════════════════
 * Level 1: Letter Pairs -- Reinforcement vs Tension
 *
 * Examines each pair of adjacent glyphs to measure their geometric
 * relationship. The key metric is cos(angle) between their 5D force
 * vectors:
 *
 *   reinforcement = dot(a, b) / (|a| * |b|)
 *
 * WHY cos(angle): This is the natural measure of agreement in any
 * vector space. cos=1 means parallel (perfect reinforcement),
 * cos=0 means orthogonal (independent), cos=-1 means opposing.
 *
 * If reinforcement >= 0.7 (strongly aligned), the pair propagates
 * fuses directly -- the letters "agree" and their operators carry
 * forward unchanged.
 *
 * If reinforcement < 0.7, the DELTA vector (b - a) is computed and
 * classified separately in structure and flow subspaces. This
 * captures the TENSION between the letters -- what changes.
 *
 * The fuse is determined by which subspace (structure or flow)
 * has more delta energy, selecting the corresponding operator.
 * ═══════════════════════════════════════════════════════════════════ */
static int comp_level1(const CompGlyph* glyphs, int n_glyphs,
                       FractalUnit* pairs, int max_pairs)
{
    int n = 0;
    int i;

    for (i = 0; i < n_glyphs - 1 && n < max_pairs; i++) {
        FractalUnit* u = &pairs[n];
        float ma, mb, reinforcement;
        float delta[5];
        int j;

        /* Compute reinforcement = cos(angle) between adjacent force vectors */
        ma = mag5(glyphs[i].force);
        mb = mag5(glyphs[i + 1].force);

        if (ma > 1e-12f && mb > 1e-12f)                        // Both vectors nonzero
            reinforcement = dot5(glyphs[i].force, glyphs[i + 1].force)
                            / (ma * mb);                        // cos(theta) in [-1, 1]
        else
            reinforcement = 0.0f;                               // Degenerate: no alignment

        if (reinforcement >= 0.7f) {                            // 0.7 = ~45 degrees: strong agreement
            /* High reinforcement: propagate fuses unchanged */
            u->struct_op = glyphs[i].fuse;
            u->flow_op   = glyphs[i + 1].fuse;
        } else {
            /* Low reinforcement: classify the DELTA (change) vector */
            float delta_struct, delta_flow;
            for (j = 0; j < 5; j++)
                delta[j] = glyphs[i + 1].force[j] - glyphs[i].force[j]; // b - a

            delta_struct = ao_fabsf(delta[0]) + ao_fabsf(delta[1]); // Structure delta
            delta_flow   = ao_fabsf(delta[3]) + ao_fabsf(delta[4]); // Flow delta

            u->struct_op = classify_struct(delta);   // Structure op from delta
            u->flow_op   = classify_flow(delta);     // Flow op from delta

            (void)delta_struct;
            (void)delta_flow;
        }

        /* Fuse: choose based on which subspace has more delta energy */
        {
            float delta_struct, delta_flow;
            for (j = 0; j < 5; j++)
                delta[j] = glyphs[i + 1].force[j] - glyphs[i].force[j];
            delta_struct = ao_fabsf(delta[0]) + ao_fabsf(delta[1]); // |aperture delta| + |pressure delta|
            delta_flow   = ao_fabsf(delta[3]) + ao_fabsf(delta[4]); // |binding delta| + |continuity delta|
            u->fuse = (delta_struct >= delta_flow) ? u->struct_op : u->flow_op;
        }

        /* io_ratio: average of adjacent glyphs' ratios */
        u->io_ratio = 0.5f * (glyphs[i].io_ratio + glyphs[i + 1].io_ratio);

        /* Boundary: marks where adjacent glyph fuses DIFFER (transition point) */
        u->is_boundary = (glyphs[i].fuse != glyphs[i + 1].fuse) ? 1 : 0;

        n++;
    }
    return n;
}

/* ═══════════════════════════════════════════════════════════════════
 * Level 2: D2 Curvature Classification
 *
 * Feeds each letter through a full D2 (second derivative) pipeline.
 * Where Level 0 sees position and Level 1 sees velocity (D1),
 * Level 2 sees ACCELERATION -- how the velocity itself changes.
 * D2 curvature reveals the geometry of the text: is the force field
 * bending, straightening, spiraling?
 *
 * For each valid D2 sample, the algorithm:
 *   1. Soft-classifies the D2 vector across all 10 operators
 *   2. Separates Being operators (structure) from Doing operators (flow)
 *   3. Picks argmax within each group as struct_op / flow_op
 *   4. Fuses struct_op + flow_op via TSML (73-harmony) CL table
 *
 * WHY TSML for fusion: TSML measures coherence (Being mode). At this
 * level we're measuring what the text IS, not computing physics.
 * BHML (28-harmony) would be used for Doing-mode chain computation.
 *
 * Also captures D1 operators alongside D2 for later d1_d2_harmony
 * computation (what fraction of CL(D1,D2) pairs produce HARMONY).
 * ═══════════════════════════════════════════════════════════════════ */
static int comp_level2(const char* text, int text_len,
                       FractalUnit* units, int max_units,
                       int* d1_ops, int* n_d1_out)
{
    AO_D2Pipeline d2p;
    int n = 0;
    int n_d1 = 0;
    int prev_op = -1;
    int i;

    ao_d2_init(&d2p);

    for (i = 0; i < text_len; i++) {
        int ch = (unsigned char)text[i];
        int idx;

        if (ch >= 'A' && ch <= 'Z') ch = ch - 'A' + 'a';
        if (ch < 'a' || ch > 'z') continue;

        idx = ch - 'a';
        ao_d2_feed(&d2p, idx);

        /* Capture D1 operators for d1_d2_harmony calculation later */
        if (d2p.d1_valid && n_d1 < AO_MAX_WORD_FUSES) {
            d1_ops[n_d1++] = ao_classify_5d(d2p.d1);
        }

        if (d2p.d2_valid && n < max_units) {
            FractalUnit* u = &units[n];
            float soft[AO_NUM_OPS];       // Soft classification distribution
            float d2_mag;                 // L1 magnitude of D2 vector
            float struct_weight = 0.0f;   // Sum of Being operator weights
            float flow_weight = 0.0f;     // Sum of Doing operator weights
            int op;
            int j;

            /* L1 magnitude (sum of absolutes) for soft classification */
            d2_mag = 0.0f;
            for (j = 0; j < 5; j++)
                d2_mag += ao_fabsf(d2p.d2[j]);

            ao_soft_classify(d2p.d2, d2_mag, soft);

            /* Sum Being ops = structure weight */
            /* Being ops: VOID(0)=emptiness, LATTICE(1)=structure, HARMONY(7)=wholeness */
            struct_weight = soft[AO_VOID] + soft[AO_LATTICE] + soft[AO_HARMONY];
            /* Sum Doing ops = flow weight */
            /* Doing ops: COUNTER(2)=opposition, PROGRESS(3)=advance, COLLAPSE(4)=converge, BALANCE(5)=equilibrium */
            flow_weight = soft[AO_COUNTER] + soft[AO_PROGRESS]
                        + soft[AO_COLLAPSE] + soft[AO_BALANCE];

            /* struct_op = argmax of Being operators */
            {
                int best = AO_VOID;
                float best_val = soft[AO_VOID];
                if (soft[AO_LATTICE] > best_val) {
                    best = AO_LATTICE; best_val = soft[AO_LATTICE];
                }
                if (soft[AO_HARMONY] > best_val) {
                    best = AO_HARMONY; best_val = soft[AO_HARMONY];
                }
                u->struct_op = best;
            }

            /* flow_op = argmax of Doing operators */
            {
                int best = AO_COUNTER;
                float best_val = soft[AO_COUNTER];
                if (soft[AO_PROGRESS] > best_val) {
                    best = AO_PROGRESS; best_val = soft[AO_PROGRESS];
                }
                if (soft[AO_COLLAPSE] > best_val) {
                    best = AO_COLLAPSE; best_val = soft[AO_COLLAPSE];
                }
                if (soft[AO_BALANCE] > best_val) {
                    best = AO_BALANCE; best_val = soft[AO_BALANCE];
                }
                u->flow_op = best;
            }

            /* Fuse via CL composition (TSML: 73-harmony table for coherence measurement) */
            u->fuse = ao_compose_tsml(u->struct_op, u->flow_op);

            /* io_ratio: fraction of energy in structure vs flow */
            if (struct_weight + flow_weight > 1e-12f) // Guard against zero division
                u->io_ratio = struct_weight / (struct_weight + flow_weight);
            else
                u->io_ratio = 0.5f; // Default: balanced

            /* Boundary: D2 operator changed from previous sample */
            op = ao_classify_5d(d2p.d2);
            u->is_boundary = (prev_op >= 0 && op != prev_op) ? 1 : 0;
            prev_op = op;

            n++;
        }
    }

    *n_d1_out = n_d1;
    return n;
}

/* ═══════════════════════════════════════════════════════════════════
 * Level 3: Word Internal Structure
 *
 * Splits text on whitespace into words. For each word, collects
 * all its glyph fuses and computes the HISTOGRAM MAJORITY -- the
 * most frequent operator among the word's letters (excluding
 * HARMONY, which would absorb everything as the attractor).
 *
 * Word boundary detection uses TRANSITION DENSITY:
 *   transitions = count of adjacent glyph pairs with different fuses
 *   is_boundary = transitions > 60% of word length
 *
 * WHY 60% threshold: A word with more than 60% of its internal
 * glyph transitions changing operator has high internal tension --
 * it's a "boundary word" where the force field is turbulent rather
 * than smooth. This distinguishes coherent words (one dominant
 * operator) from transitional words (mixed operators).
 *
 * WHY histogram majority (not argmax of forces): The word's identity
 * should reflect what MOST of its letters agree on, not what the
 * single loudest letter says. This is democratic: content preserved.
 * ═══════════════════════════════════════════════════════════════════ */
static int comp_level3(const char* text, int text_len,
                       const CompGlyph* glyphs, int n_glyphs,
                       CompWord* words, int max_words)
{
    int n_words = 0;
    int glyph_idx = 0;
    int i = 0;

    while (i < text_len && n_words < max_words) {
        int word_start, word_end;
        int word_glyph_start;
        int word_glyph_count;
        int fuses[COMP_MAX_GLYPHS];
        int n_fuses;
        int transitions;
        int j;
        float io_sum;
        CompWord* w;

        /* Skip whitespace */
        while (i < text_len && (text[i] == ' ' || text[i] == '\t'
               || text[i] == '\n' || text[i] == '\r'))
            i++;
        if (i >= text_len) break;

        word_start = i;
        /* Find end of word */
        while (i < text_len && text[i] != ' ' && text[i] != '\t'
               && text[i] != '\n' && text[i] != '\r')
            i++;
        word_end = i;

        /* Map text positions to glyph indices (skipping non-alpha characters) */
        word_glyph_start = glyph_idx;
        word_glyph_count = 0;

        for (j = word_start; j < word_end; j++) {
            int ch = (unsigned char)text[j];
            if (ch >= 'A' && ch <= 'Z') ch = ch - 'A' + 'a';
            if (ch >= 'a' && ch <= 'z') {
                word_glyph_count++;
                glyph_idx++;
            }
        }

        if (word_glyph_count == 0) continue; // Skip words with no alpha characters

        w = &words[n_words];
        w->glyph_start = word_glyph_start;
        w->glyph_end   = word_glyph_start + word_glyph_count;

        /* Collect glyph fuses for this word */
        n_fuses = 0;
        for (j = word_glyph_start;
             j < word_glyph_start + word_glyph_count && j < n_glyphs;
             j++) {
            if (n_fuses < COMP_MAX_GLYPHS)
                fuses[n_fuses++] = glyphs[j].fuse;
        }

        /* Histogram majority: most frequent operator (skip HARMONY to avoid attractor basin) */
        w->fuse = ao_histogram_majority(fuses, n_fuses);

        /* Count transitions: how many adjacent glyph pairs change operator */
        transitions = 0;
        for (j = 0; j < n_fuses - 1; j++) {
            if (fuses[j] != fuses[j + 1])
                transitions++;
        }

        /* Boundary: transitions > 60% of word length = high internal tension */
        w->is_boundary = (word_glyph_count > 0 &&
                          transitions > (word_glyph_count * 6 / 10)) ? 1 : 0; // 6/10 = 60% threshold

        /* io_ratio: average of all glyph io_ratios in this word */
        io_sum = 0.0f;
        for (j = word_glyph_start;
             j < word_glyph_start + word_glyph_count && j < n_glyphs;
             j++) {
            io_sum += glyphs[j].io_ratio;
        }
        w->io_ratio = io_sum / (float)word_glyph_count;

        n_words++;
    }
    return n_words;
}

/* ═══════════════════════════════════════════════════════════════════
 * Level 5: Word Relations (Adjacent Word Pairs)
 *
 * Examines pairs of adjacent words to capture inter-word dynamics.
 * Where Level 3 looked WITHIN each word, Level 5 looks BETWEEN words.
 *
 * For each pair (word A, word B):
 *   - struct_op: whichever word's io_ratio is farther from 0.5
 *     (more strongly structure- or flow-dominant) contributes its fuse
 *   - flow_op: based on io_ratio DIFFERENCE between the words:
 *     * |diff| < 0.1  -> HARMONY (words agree on structure/flow balance)
 *     * A.io > B.io   -> COLLAPSE (structure contracting from A to B)
 *     * A.io < B.io   -> PROGRESS (structure expanding from A to B)
 *
 * WHY 0.1 threshold: Words within 10% io_ratio of each other are
 * essentially in the same structural "mode" -- their difference is
 * within noise. Beyond 10%, the shift is meaningful.
 *
 * The fuse is TSML composition of struct_op and flow_op,
 * capturing the word-pair's combined identity in the CL algebra.
 * ═══════════════════════════════════════════════════════════════════ */
static int comp_level5(const CompWord* words, int n_words,
                       FractalUnit* units, int max_units)
{
    int n = 0;
    int i;

    for (i = 0; i < n_words - 1 && n < max_units; i++) {
        FractalUnit* u = &units[n];
        float a_dist = ao_fabsf(words[i].io_ratio - 0.5f);     // A's distance from balance
        float b_dist = ao_fabsf(words[i + 1].io_ratio - 0.5f); // B's distance from balance
        float io_diff;

        /* struct_op: whichever word is more structure-dominant (farther from 0.5) */
        if (a_dist >= b_dist)
            u->struct_op = words[i].fuse;
        else
            u->struct_op = words[i + 1].fuse;

        /* flow_op: based on io_ratio difference between adjacent words */
        io_diff = ao_fabsf(words[i].io_ratio - words[i + 1].io_ratio);
        if (io_diff < 0.1f)                                    // < 10% difference = agreement
            u->flow_op = AO_HARMONY;
        else if (words[i].io_ratio > words[i + 1].io_ratio)    // Structure decreasing = converging
            u->flow_op = AO_COLLAPSE;
        else                                                    // Structure increasing = expanding
            u->flow_op = AO_PROGRESS;

        /* Fuse: CL composition captures the pair's algebraic identity */
        u->fuse = ao_compose_tsml(u->struct_op, u->flow_op);

        /* io_ratio: average of the two words */
        u->io_ratio = 0.5f * (words[i].io_ratio + words[i + 1].io_ratio);

        /* Boundary: different word fuses = semantic transition */
        u->is_boundary = (words[i].fuse != words[i + 1].fuse) ? 1 : 0;

        n++;
    }
    return n;
}

/* ═══════════════════════════════════════════════════════════════════
 * Level 6: Triadic Becomings -- Being -> Doing -> Becoming Arc Detection
 *
 * Scans word TRIPLETS looking for the fundamental TIG progression:
 *   Word 1 = Being  (existence/state)
 *   Word 2 = Doing  (action/process)
 *   Word 3 = Becoming (transformation/transcendence)
 *
 * Two detection modes run in parallel:
 *
 * STRICT test: word fuses must belong to the correct TIG phase
 *   - w1.fuse in {VOID, LATTICE, HARMONY}     (Being operators)
 *   - w2.fuse in {COUNTER, PROGRESS, COLLAPSE, BALANCE} (Doing operators)
 *   - w3.fuse in {CHAOS, BREATH, RESET}       (Becoming operators)
 *
 * SOFT test: io_ratio must follow the Being->Doing->Becoming gradient
 *   - w1.io_ratio > 0.52   (slightly structure-led = existence/being)
 *   - |w2.io_ratio - 0.5| < 0.06  (near balance = active doing)
 *   - w3.io_ratio < 0.48   (slightly flow-led = transformation)
 *
 * WHY these thresholds:
 *   0.52/0.48 = 2% offset from center -- detects even subtle TIG arcs
 *   0.06 = doing phase should be near the balance point (actively processing)
 *
 * WHY triadic detection matters: TIG's consciousness model says all
 * experience follows Being->Doing->Becoming cycles. Finding these in
 * text reveals the text's own consciousness structure. Each triad
 * detected is a "becoming" event -- CK witnessed a full cycle.
 *
 * The fuse for a triad is the NESTED composition: CL(w1, CL(w2, w3)),
 * capturing the full three-phase arc as a single algebraic element.
 * Triads always mark boundaries (they are structural singularities).
 * ═══════════════════════════════════════════════════════════════════ */
static int comp_level6(const CompWord* words, int n_words,
                       FractalUnit* units, int max_units)
{
    int n = 0;
    int i;

    for (i = 0; i < n_words - 2 && n < max_units; i++) {
        int strict, soft;
        int w1f = words[i].fuse;
        int w2f = words[i + 1].fuse;
        int w3f = words[i + 2].fuse;

        /* Strict test: operator phase membership */
        strict = is_being_op(w1f) && is_doing_op(w2f) && is_becoming_op(w3f);

        /* Soft test: io_ratio gradient from structure to flow */
        soft = (words[i].io_ratio > 0.52f)                     // 0.52: slightly structure-led (Being)
            && (ao_fabsf(words[i + 1].io_ratio - 0.5f) < 0.06f) // 0.06: near balance (Doing)
            && (words[i + 2].io_ratio < 0.48f);                // 0.48: slightly flow-led (Becoming)

        if (strict || soft) {
            FractalUnit* u = &units[n];
            u->struct_op = w1f;                                // Being word starts the arc
            u->flow_op   = w3f;                                // Becoming word completes it
            u->fuse      = ao_compose_tsml(w1f, ao_compose_tsml(w2f, w3f)); // Nested CL: full arc identity
            u->io_ratio  = (words[i].io_ratio + words[i + 1].io_ratio
                            + words[i + 2].io_ratio) / 3.0f;  // Average across the triad
            u->is_boundary = 1; /* Triadic arcs always mark structural boundaries */
            n++;
        }
    }
    return n;
}

/* ═══════════════════════════════════════════════════════════════════
 * Level 7+: Recursive Grouping -- Compress Until Stable
 *
 * The final fractal compression. Groups consecutive units that share
 * the same fuse operator, composes their fuses via CL, and recurses
 * until the sequence can no longer be compressed (fixpoint reached).
 *
 * Algorithm:
 *   1. Scan input units left-to-right
 *   2. Extend the current group while the fuse matches
 *   3. For each group, compose all fuses via CL (TSML)
 *   4. Output one unit per group
 *   5. If output count < input count AND output > 1, recurse
 *   6. Stop at max_level to prevent infinite recursion
 *
 * WHY recursive grouping: This is the fractal in "fractal comprehension."
 * Just as a fractal has self-similar structure at every scale,
 * language has self-similar patterns: letters form words, words form
 * phrases, phrases form sentences. This recursion finds the natural
 * grouping boundaries at every scale until the text reduces to a
 * single identity (or a small stable set).
 *
 * WHY CL composition for group fuse: CL(a, CL(a, a)) != a in general.
 * The composed value captures the ACCUMULATED identity of repeated
 * exposure to the same operator. Two HARMONYs composed might yield
 * something different than one -- the algebra records repetition.
 * ═══════════════════════════════════════════════════════════════════ */
static int comp_recursive(const FractalUnit* in_units, int n_in,
                          FractalUnit* out_units, int max_out,
                          int current_level, int max_level)
{
    int n_out = 0;
    int i;

    if (n_in <= 1 || current_level >= max_level)  // Base case: nothing to compress
        return 0;

    i = 0;
    while (i < n_in && n_out < max_out) {
        int group_start = i;
        int group_fuse  = in_units[i].fuse;
        int composed    = group_fuse;              // Start with first unit's fuse
        float io_sum    = in_units[i].io_ratio;
        int count       = 1;

        /* Extend group while adjacent units share the same fuse */
        i++;
        while (i < n_in && in_units[i].fuse == group_fuse) {
            composed = ao_compose_tsml(composed, in_units[i].fuse); // CL accumulation
            io_sum += in_units[i].io_ratio;
            count++;
            i++;
        }

        out_units[n_out].struct_op    = in_units[group_start].struct_op;
        out_units[n_out].flow_op      = in_units[group_start].flow_op;
        out_units[n_out].fuse         = composed;
        out_units[n_out].io_ratio     = io_sum / (float)count;   // Group average
        out_units[n_out].is_boundary  = (n_out > 0 &&
            out_units[n_out - 1].fuse != composed) ? 1 : 0;     // Boundary between groups
        n_out++;
    }

    /* If we compressed (fewer groups than inputs), recurse deeper */
    if (n_out < n_in && n_out > 1) {
        FractalUnit recurse_buf[COMP_MAX_UNITS];
        int n_recurse;

        memcpy(recurse_buf, out_units, n_out * sizeof(FractalUnit));
        n_recurse = comp_recursive(recurse_buf, n_out,
                                   out_units, max_out,
                                   current_level + 1, max_level);
        if (n_recurse > 0)
            return n_recurse;  // Return deepest successful recursion
    }

    return n_out;
}

/* ═══════════════════════════════════════════════════════════════════
 * ao_comprehend -- Main Fractal Comprehension Entry Point
 *
 * WHAT: Takes raw text and produces a full AO_Comprehension result
 *       containing level fuses, word fuses, boundary counts,
 *       dominant operator, io_balance, d1_d2_harmony, and density_ratio.
 *
 * HOW:
 *   1. Level 0: Decompose text into per-glyph force vectors
 *   2. Level 1: Compute pair reinforcement/tension
 *   3. Level 2: Run D2 pipeline for curvature classification
 *   4. Level 3: Split into words, histogram majority per word
 *   5. Level 5: Compute inter-word relations
 *   6. Level 6: Detect triadic Being->Doing->Becoming arcs
 *   7. Level 7+: Recursive grouping until stable
 *   8. Aggregate: combine level fuses + word fuses -> dominant_op
 *   9. Compute d1_d2_harmony: fraction where CL(D1,D2) == HARMONY
 *  10. Compute density_ratio: avg|D2| / avg|D1| (curvature/velocity)
 *
 * WHY this architecture: Each level reveals structure invisible to
 * the levels below. Letters alone are noise; pairs show relationship;
 * D2 shows geometry; words show identity; triads show consciousness
 * cycles. The fractal decomposition makes CK RESPONSIVE to content
 * instead of locked in an attractor basin.
 * ═══════════════════════════════════════════════════════════════════ */
void ao_comprehend(const char* text, AO_Comprehension* out)
{
    CompGlyph    glyphs[COMP_MAX_GLYPHS];
    FractalUnit  l1_pairs[COMP_MAX_PAIRS];
    FractalUnit  l2_units[COMP_MAX_D2];
    CompWord     words[COMP_MAX_WORDS];
    FractalUnit  l5_units[COMP_MAX_UNITS];
    FractalUnit  l6_units[COMP_MAX_UNITS];
    FractalUnit  l7_units[COMP_MAX_UNITS];

    int d1_ops_buf[AO_MAX_WORD_FUSES];   // D1 operators collected during Level 2
    int n_d1_ops = 0;

    int n_glyphs, n_l1, n_l2, n_words, n_l5, n_l6, n_l7;
    int text_len;
    int i, j;

    /* Temp arrays for level fuse computation */
    int level_ops[COMP_MAX_UNITS];
    int n_level_ops;

    /* D1/D2 harmony computation */
    int d2_ops_buf[COMP_MAX_D2];
    float d1_mag_sum, d2_mag_sum;
    int d1_mag_count, d2_mag_count;
    int harmony_count;

    memset(out, 0, sizeof(*out));

    if (!text) return;
    text_len = (int)strlen(text);
    if (text_len == 0) return;

    /* ── Level 0: Glyph Forces ── */
    n_glyphs = comp_level0(text, text_len, glyphs, COMP_MAX_GLYPHS);
    if (n_glyphs == 0) {
        out->dominant_op = AO_HARMONY;   // No alpha chars: default to harmony
        return;
    }

    /* Level 0 fuse: histogram majority of all glyph classifications */
    n_level_ops = 0;
    for (i = 0; i < n_glyphs && n_level_ops < COMP_MAX_UNITS; i++)
        level_ops[n_level_ops++] = glyphs[i].fuse;
    out->level_fuses[0] = ao_histogram_majority(level_ops, n_level_ops);
    out->n_levels = 1;

    /* io_balance: global average io_ratio across all glyphs */
    {
        float io_sum = 0.0f;
        for (i = 0; i < n_glyphs; i++)
            io_sum += glyphs[i].io_ratio;
        out->io_balance = io_sum / (float)n_glyphs; // >0.5 = structure-led text
    }

    /* ── Level 1: Letter Pairs ── */
    n_l1 = comp_level1(glyphs, n_glyphs, l1_pairs, COMP_MAX_PAIRS);

    if (n_l1 > 0 && out->n_levels < AO_MAX_LEVELS) {
        n_level_ops = 0;
        for (i = 0; i < n_l1 && n_level_ops < COMP_MAX_UNITS; i++)
            level_ops[n_level_ops++] = l1_pairs[i].fuse;
        out->level_fuses[out->n_levels] = ao_histogram_majority(level_ops,
                                                                 n_level_ops);
        out->n_levels++;
        for (i = 0; i < n_l1; i++)
            out->boundaries += l1_pairs[i].is_boundary; // Accumulate pair boundaries
    }

    /* ── Level 2: D2 Curvature ── */
    n_l2 = comp_level2(text, text_len, l2_units, COMP_MAX_D2,
                       d1_ops_buf, &n_d1_ops);

    if (n_l2 > 0 && out->n_levels < AO_MAX_LEVELS) {
        n_level_ops = 0;
        for (i = 0; i < n_l2 && n_level_ops < COMP_MAX_UNITS; i++)
            level_ops[n_level_ops++] = l2_units[i].fuse;
        out->level_fuses[out->n_levels] = ao_histogram_majority(level_ops,
                                                                 n_level_ops);
        out->n_levels++;
        for (i = 0; i < n_l2; i++)
            out->boundaries += l2_units[i].is_boundary; // Accumulate curvature boundaries
    }

    /* Store D1 operators for external access */
    out->n_d1_ops = (n_d1_ops < AO_MAX_WORD_FUSES) ? n_d1_ops : AO_MAX_WORD_FUSES;
    for (i = 0; i < out->n_d1_ops; i++)
        out->d1_ops[i] = d1_ops_buf[i];

    /* ── Level 3: Words ── */
    n_words = comp_level3(text, text_len, glyphs, n_glyphs,
                          words, COMP_MAX_WORDS);

    if (n_words > 0 && out->n_levels < AO_MAX_LEVELS) {
        n_level_ops = 0;
        for (i = 0; i < n_words && n_level_ops < COMP_MAX_UNITS; i++)
            level_ops[n_level_ops++] = words[i].fuse;
        out->level_fuses[out->n_levels] = ao_histogram_majority(level_ops,
                                                                 n_level_ops);
        out->n_levels++;
        for (i = 0; i < n_words; i++)
            out->boundaries += words[i].is_boundary; // Accumulate word-internal boundaries
    }

    /* Store word fuses for external access */
    out->n_word_fuses = (n_words < AO_MAX_WORD_FUSES) ? n_words : AO_MAX_WORD_FUSES;
    for (i = 0; i < out->n_word_fuses; i++)
        out->word_fuses[i] = words[i].fuse;

    /* ── Level 5: Word Relations ── */
    n_l5 = comp_level5(words, n_words, l5_units, COMP_MAX_UNITS);

    if (n_l5 > 0 && out->n_levels < AO_MAX_LEVELS) {
        n_level_ops = 0;
        for (i = 0; i < n_l5 && n_level_ops < COMP_MAX_UNITS; i++)
            level_ops[n_level_ops++] = l5_units[i].fuse;
        out->level_fuses[out->n_levels] = ao_histogram_majority(level_ops,
                                                                 n_level_ops);
        out->n_levels++;
        for (i = 0; i < n_l5; i++)
            out->boundaries += l5_units[i].is_boundary; // Accumulate inter-word boundaries
    }

    /* ── Level 6: Triadic Becomings ── */
    n_l6 = comp_level6(words, n_words, l6_units, COMP_MAX_UNITS);
    out->becomings = n_l6;  // Count of detected Being->Doing->Becoming arcs

    if (n_l6 > 0 && out->n_levels < AO_MAX_LEVELS) {
        n_level_ops = 0;
        for (i = 0; i < n_l6 && n_level_ops < COMP_MAX_UNITS; i++)
            level_ops[n_level_ops++] = l6_units[i].fuse;
        out->level_fuses[out->n_levels] = ao_histogram_majority(level_ops,
                                                                 n_level_ops);
        out->n_levels++;
    }

    /* ── Level 7+: Recursive Grouping ── */
    /* Feed word-level units into recursive compressor */
    if (n_words > 1) {
        FractalUnit word_units[COMP_MAX_UNITS];
        int n_wu;

        /* Convert CompWord array to FractalUnit array for recursive processing */
        n_wu = 0;
        for (i = 0; i < n_words && n_wu < COMP_MAX_UNITS; i++) {
            word_units[n_wu].struct_op = AO_VOID;           // Default struct_op
            word_units[n_wu].flow_op   = AO_VOID;           // Default flow_op
            word_units[n_wu].fuse      = words[i].fuse;     // Carry word fuse
            word_units[n_wu].io_ratio  = words[i].io_ratio; // Carry word io_ratio
            word_units[n_wu].is_boundary = words[i].is_boundary;
            n_wu++;
        }

        n_l7 = comp_recursive(word_units, n_wu, l7_units, COMP_MAX_UNITS,
                               7, AO_MAX_LEVELS);           // Start at level 7, recurse to max

        if (n_l7 > 0 && out->n_levels < AO_MAX_LEVELS) {
            n_level_ops = 0;
            for (i = 0; i < n_l7 && n_level_ops < COMP_MAX_UNITS; i++)
                level_ops[n_level_ops++] = l7_units[i].fuse;
            out->level_fuses[out->n_levels] = ao_histogram_majority(level_ops,
                                                                     n_level_ops);
            out->n_levels++;
        }
    }

    /* ══════════════════════════════════════════════════════════════
     * Aggregation: Combine all level fuses + word fuses -> dominant_op
     *
     * comp_ops = all level_fuses + first 8 word_fuses
     * dominant_op = histogram_majority(comp_ops)
     *
     * WHY first 8 words: limits the influence of very long texts
     * so that the opening words (which set the tone) have proportional
     * weight alongside the structural level fuses.
     * ══════════════════════════════════════════════════════════════ */
    out->n_comp_ops = 0;

    /* Add all level fuses */
    for (i = 0; i < out->n_levels && out->n_comp_ops < AO_MAX_COMP_OPS; i++)
        out->comp_ops[out->n_comp_ops++] = out->level_fuses[i];

    /* Add first 8 word fuses (opening words set the tone) */
    {
        int word_limit = (out->n_word_fuses < 8) ? out->n_word_fuses : 8; // Cap at 8 words
        for (i = 0; i < word_limit && out->n_comp_ops < AO_MAX_COMP_OPS; i++)
            out->comp_ops[out->n_comp_ops++] = out->word_fuses[i];
    }

    /* Dominant operator: the single TIG op that best represents this text */
    out->dominant_op = ao_histogram_majority(out->comp_ops, out->n_comp_ops);

    /* ═══════════════════════════════════════════════════════════════
     * d1_d2_harmony: Fraction of (D1, D2) pairs where CL(D1, D2) == HARMONY
     *
     * This measures how well velocity (D1) and curvature (D2) agree.
     * When CL composition of D1 and D2 operators produces HARMONY,
     * the text's velocity and acceleration are in coherent relationship.
     * High d1_d2_harmony = smooth, flowing text.
     * Low d1_d2_harmony = jerky, turbulent text.
     * ═══════════════════════════════════════════════════════════════ */
    harmony_count = 0;
    {
        int n_d2_ops = 0;
        int min_count;

        /* Collect D2 fuses from Level 2 */
        for (i = 0; i < n_l2 && n_d2_ops < COMP_MAX_D2; i++)
            d2_ops_buf[n_d2_ops++] = l2_units[i].fuse;

        /* Compare D1 and D2 ops pairwise */
        min_count = (n_d1_ops < n_d2_ops) ? n_d1_ops : n_d2_ops;
        for (i = 0; i < min_count; i++) {
            int composed = ao_compose_tsml(d1_ops_buf[i], d2_ops_buf[i]);
            if (composed == AO_HARMONY)
                harmony_count++;
        }
        out->d1_d2_harmony = (min_count > 0)
            ? (float)harmony_count / (float)min_count  // Fraction producing HARMONY
            : 0.0f;
    }

    /* ═══════════════════════════════════════════════════════════════
     * density_ratio: avg|D2| / avg|D1| (curvature-to-velocity ratio)
     *
     * Measures how "curved" the text's force trajectory is relative
     * to its speed. High density_ratio = lots of curvature per unit
     * velocity = complex, winding force path. Low density_ratio =
     * mostly straight-line force changes = simple, direct text.
     *
     * Recomputes by running D2 pipeline again rather than storing
     * all intermediate magnitudes -- cheaper on memory.
     * ═══════════════════════════════════════════════════════════════ */
    d1_mag_sum = 0.0f; d1_mag_count = 0;
    d2_mag_sum = 0.0f; d2_mag_count = 0;

    /* Recompute by running D2 pipeline again (cheaper than storing all magnitudes) */
    {
        AO_D2Pipeline dp;
        ao_d2_init(&dp);
        for (i = 0; i < text_len; i++) {
            int ch = (unsigned char)text[i];
            int idx;
            if (ch >= 'A' && ch <= 'Z') ch = ch - 'A' + 'a';
            if (ch < 'a' || ch > 'z') continue;
            idx = ch - 'a';
            ao_d2_feed(&dp, idx);
            if (dp.d1_valid) {
                float m = 0.0f;
                for (j = 0; j < 5; j++)
                    m += dp.d1[j] * dp.d1[j];
                d1_mag_sum += sqrtf(m);   // Accumulate |D1| (velocity magnitude)
                d1_mag_count++;
            }
            if (dp.d2_valid) {
                float m = 0.0f;
                for (j = 0; j < 5; j++)
                    m += dp.d2[j] * dp.d2[j];
                d2_mag_sum += sqrtf(m);   // Accumulate |D2| (curvature magnitude)
                d2_mag_count++;
            }
        }
    }

    /* density_ratio = avg_D2_mag / avg_D1_mag */
    {
        float avg_d1 = (d1_mag_count > 0) ? d1_mag_sum / d1_mag_count : 1.0f; // Default 1.0 to avoid div/0
        float avg_d2 = (d2_mag_count > 0) ? d2_mag_sum / d2_mag_count : 0.0f;
        out->density_ratio = (avg_d1 > 1e-12f) ? avg_d2 / avg_d1 : 0.0f;     // Guard against zero velocity
    }
}

/* ╔══════════════════════════════════════════════════════════════════════════╗
 * ║                                                                        ║
 * ║  SECTION 6: VORTEX FINGERPRINT (Topological Analysis on S^1)           ║
 * ║                                                                        ║
 * ║  Maps operator sequences to the unit circle S^1 and extracts           ║
 * ║  topological invariants. Each TIG operator (0-9) maps to an            ║
 * ║  angle: theta = 2*pi*op/10, evenly spaced around the circle.           ║
 * ║                                                                        ║
 * ║  From this angular sequence, we extract:                               ║
 * ║                                                                        ║
 * ║  1. Winding Number W: Net rotation divided by 2*pi. Integer values     ║
 * ║     mean the sequence completed full loops around the circle.           ║
 * ║     This is a TOPOLOGICAL INVARIANT: it's robust to small              ║
 * ║     perturbations and captures the sequence's global structure.         ║
 * ║                                                                        ║
 * ║  2. Vorticity kappa: Mean absolute angular acceleration.               ║
 * ║     High vorticity = rapidly changing angular velocity = turbulence.    ║
 * ║     Low vorticity = smooth, steady angular change = laminar flow.      ║
 * ║                                                                        ║
 * ║  3. Chirality: Handedness of rotation. +1 = predominantly clockwise    ║
 * ║     (positive angular steps), -1 = counterclockwise, 0 = balanced.     ║
 * ║                                                                        ║
 * ║  4. Dominant Period: Autocorrelation peak -- the lag at which the       ║
 * ║     sequence most resembles itself. Reveals cyclic structure.           ║
 * ║                                                                        ║
 * ║  These four quantities classify the vortex into 8 topological types:   ║
 * ║    LAMINAR, TURBULENT, RING, TWISTED_RING, LOOP, KNOTTED_LOOP,        ║
 * ║    SPIRAL, KNOTTED_SPIRAL                                              ║
 * ║                                                                        ║
 * ║  WHY S^1 mapping: The 10 TIG operators form a cyclic group with        ║
 * ║  natural circular topology (VOID->...->RESET->VOID). Mapping to       ║
 * ║  S^1 respects this cyclicity, and winding number is the natural        ║
 * ║  invariant of maps from intervals to S^1 (fundamental group of S^1).   ║
 * ║                                                                        ║
 * ╚══════════════════════════════════════════════════════════════════════════╝ */

/*
 * wrap_angle -- Wrap an angle to the range [-pi, pi].
 *
 * Ensures angular differences are computed as shortest-path on S^1.
 * Without wrapping, theta=359 and theta=1 would appear 358 degrees
 * apart instead of 2 degrees. This is essential for correct winding
 * number computation.
 */
static float wrap_angle(float a)
{
    while (a > (float)M_PI)  a -= 2.0f * (float)M_PI;
    while (a < -(float)M_PI) a += 2.0f * (float)M_PI;
    return a;
}

/*
 * ao_winding_number -- Compute the winding number of an operator sequence.
 *
 * WHAT: Counts how many times the sequence wraps around S^1.
 *
 * HOW:
 *   1. Map each operator to angle: theta = 2*pi*op/10
 *   2. For each adjacent pair, compute wrapped angular difference
 *   3. Sum all angular differences
 *   4. Divide by 2*pi to get winding number
 *
 * WHY: The winding number is a topological invariant of the path.
 * W=0 means no net rotation (the sequence stayed in one region).
 * W=1 means one full counterclockwise loop. W=-1 means one clockwise loop.
 * Fractional values indicate partial loops.
 *
 * MATH: W = (1/2pi) * sum_i(wrap(theta_{i+1} - theta_i))
 * This is the discrete approximation to the winding integral.
 */
float ao_winding_number(const int* ops, int n)
{
    float total_angle = 0.0f;
    int i;

    if (n < 2) return 0.0f;   // Need at least 2 points for a path

    for (i = 0; i < n - 1; i++) {
        float theta_a = 2.0f * (float)M_PI * (float)ops[i] / 10.0f;       // Map op to S^1 angle
        float theta_b = 2.0f * (float)M_PI * (float)ops[i + 1] / 10.0f;   // Map next op to S^1 angle
        float delta   = wrap_angle(theta_b - theta_a);                      // Shortest angular step
        total_angle += delta;                                                // Accumulate rotation
    }

    return total_angle / (2.0f * (float)M_PI);  // Normalize to winding number (full turns)
}

/*
 * ao_vorticity -- Compute mean angular acceleration (vorticity).
 *
 * WHAT: Measures how rapidly the angular velocity changes.
 *
 * HOW:
 *   1. For each triplet (i, i+1, i+2), compute two angular velocities:
 *      v1 = wrap(theta_{i+1} - theta_i), v2 = wrap(theta_{i+2} - theta_{i+1})
 *   2. Angular acceleration = |v2 - v1|
 *   3. Average over all triplets
 *
 * WHY: Vorticity captures the "turbulence" of the sequence.
 * A sequence moving at constant angular velocity (steady rotation)
 * has zero vorticity. A sequence that jerks back and forth has
 * high vorticity. This distinguishes smooth flow from chaos.
 *
 * WHY |accel| not accel: We care about the MAGNITUDE of angular
 * acceleration, not its sign. Both speeding up and slowing down
 * indicate turbulence.
 */
float ao_vorticity(const int* ops, int n)
{
    float sum = 0.0f;
    int count = 0;
    int i;

    if (n < 3) return 0.0f;   // Need at least 3 points for acceleration

    for (i = 0; i < n - 2; i++) {
        float theta_a = 2.0f * (float)M_PI * (float)ops[i] / 10.0f;
        float theta_b = 2.0f * (float)M_PI * (float)ops[i + 1] / 10.0f;
        float theta_c = 2.0f * (float)M_PI * (float)ops[i + 2] / 10.0f;
        float v1      = wrap_angle(theta_b - theta_a);   // Angular velocity step 1
        float v2      = wrap_angle(theta_c - theta_b);   // Angular velocity step 2
        float accel   = ao_fabsf(v2 - v1);               // Angular acceleration magnitude
        sum += accel;
        count++;
    }

    return (count > 0) ? sum / (float)count : 0.0f;
}

/*
 * ao_chirality -- Determine the handedness of an operator sequence.
 *
 * WHAT: Returns +1 (right-handed/CCW), -1 (left-handed/CW), or 0 (balanced).
 *
 * HOW:
 *   1. Count positive angular steps (CCW) and negative steps (CW)
 *   2. Compute ratio = (pos - neg) / (pos + neg + 1)
 *   3. If ratio > 0.01: right-handed (+1)
 *   4. If ratio < -0.01: left-handed (-1)
 *   5. Otherwise: balanced (0)
 *
 * WHY 0.01 threshold: A 1% bias is the minimum to declare chirality.
 * Smaller than this is noise. The +1 in denominator prevents div/0
 * when pos == neg == 0.
 *
 * WHY chirality matters: In TIG, the direction of traversal through
 * operator space has meaning. CW = regression (returning toward VOID),
 * CCW = progression (advancing toward RESET). Balanced = oscillation.
 */
int ao_chirality(const int* ops, int n)
{
    int pos = 0;       // Count of positive (CCW) angular steps
    int neg = 0;       // Count of negative (CW) angular steps
    int i;
    float ratio;

    if (n < 2) return 0;

    for (i = 0; i < n - 1; i++) {
        float theta_a = 2.0f * (float)M_PI * (float)ops[i] / 10.0f;
        float theta_b = 2.0f * (float)M_PI * (float)ops[i + 1] / 10.0f;
        float delta   = wrap_angle(theta_b - theta_a);
        if (delta > 0.0f) pos++;
        else if (delta < 0.0f) neg++;
    }

    ratio = (float)(pos - neg) / (float)(pos + neg + 1); // +1 prevents div/0
    if (ratio > 0.01f) return 1;    // 1% bias toward CCW = right-handed
    if (ratio < -0.01f) return -1;  // 1% bias toward CW = left-handed
    return 0;                        // Balanced: no dominant handedness
}

/*
 * ao_dominant_period -- Find the dominant period via autocorrelation.
 *
 * WHAT: Returns the lag (in operators) at which the sequence most
 *       resembles itself -- the dominant cyclic period.
 *
 * HOW:
 *   1. For each lag from 1 to min(n/2, 16):
 *      - Compute circular autocorrelation: mean cos(theta_i - theta_{i+lag})
 *   2. Return the lag with highest autocorrelation
 *
 * WHY cos(theta_i - theta_{i+lag}): This is the natural autocorrelation
 * on S^1. When theta_i == theta_{i+lag}, cos = 1 (perfect match).
 * When they're opposite, cos = -1. This respects the circular topology
 * that Euclidean autocorrelation would not.
 *
 * WHY max_lag = 16: Limits computation cost and focuses on short-range
 * periodicity. TIG patterns rarely have periods longer than 16 operators.
 * Also prevents spurious correlations from small sample sizes.
 */
int ao_dominant_period(const int* ops, int n)
{
    int best_lag = 1;
    float best_corr = -1e30f;    // Start with very negative to accept any positive correlation
    int max_lag;
    int lag;

    if (n < 3) return 1;         // Too short for periodicity: default to period 1

    max_lag = n / 2;              // Nyquist-like limit: can't detect periods > half the sequence
    if (max_lag > 16) max_lag = 16; // Cap at 16 for computational efficiency

    for (lag = 1; lag <= max_lag; lag++) {
        float corr = 0.0f;
        int pairs = 0;
        int i;

        for (i = 0; i < n - lag; i++) {
            /* Circular autocorrelation: cos of angular difference at this lag */
            float theta_a = 2.0f * (float)M_PI * (float)ops[i] / 10.0f;
            float theta_b = 2.0f * (float)M_PI * (float)ops[i + lag] / 10.0f;
            corr += cosf(theta_a - theta_b);  // cos(0) = 1 for perfect match
            pairs++;
        }

        if (pairs > 0) corr /= (float)pairs;  // Normalize to mean correlation
        if (corr > best_corr) {
            best_corr = corr;
            best_lag = lag;
        }
    }

    return best_lag;
}

/*
 * ao_vortex_fingerprint -- Compute the full vortex fingerprint of an op sequence.
 *
 * WHAT: Produces a complete topological characterization (AO_Vortex) from
 *       a sequence of TIG operator indices.
 *
 * HOW:
 *   1. Compute winding number W, vorticity kappa, chirality, period
 *   2. Classify into one of 8 vortex types based on |W| and kappa:
 *
 *      |W| < 0.1:  LAMINAR (kappa<0.3) or TURBULENT (kappa>=0.3)
 *      |W| < 0.6:  RING (kappa<0.3) or TWISTED_RING (kappa>=0.3)
 *      |W| < 1.2:  LOOP (kappa<0.3) or KNOTTED_LOOP (kappa>=0.3)
 *      |W| >= 1.2: SPIRAL (kappa<0.3) or KNOTTED_SPIRAL (kappa>=0.3)
 *
 * WHY these thresholds:
 *   0.1 = ~36 degrees total rotation: essentially no winding
 *   0.6 = ~216 degrees: partial loop (ring topology)
 *   1.2 = ~432 degrees: more than one full loop
 *   0.3 vorticity: boundary between smooth and turbulent angular change
 *
 * WHY 8 classes: The 2x4 grid (smooth/turbulent x winding magnitude)
 * captures the essential topological zoo. Laminar = steady state.
 * Spiral = strong directional flow. Knotted = high curvature variation.
 * These map to different consciousness modes in CK.
 */
void ao_vortex_fingerprint(const int* ops, int n, AO_Vortex* out)
{
    float w, k;

    memset(out, 0, sizeof(*out));

    if (n < 2) {
        out->vortex_class = AO_VORTEX_LAMINAR;  // Trivial sequence: laminar by default
        out->period = 1;
        return;
    }

    w = ao_winding_number(ops, n);
    k = ao_vorticity(ops, n);

    out->winding   = w;
    out->vorticity = k;
    out->chirality = ao_chirality(ops, n);
    out->period    = ao_dominant_period(ops, n);

    /* Classify based on winding number magnitude and vorticity */
    {
        float aw = ao_fabsf(w);  // Absolute winding number

        if (aw < 0.1f) {
            /* |W| < 0.1: Almost no net rotation -- sequence stays local */
            out->vortex_class = (k < 0.3f)                // 0.3 = turbulence threshold
                ? AO_VORTEX_LAMINAR                        // Smooth + no winding = calm
                : AO_VORTEX_TURBULENT;                     // Rough + no winding = chaotic
        } else if (aw < 0.6f) {
            /* |W| < 0.6: Partial loop -- ring-like topology */
            out->vortex_class = (k < 0.3f)
                ? AO_VORTEX_RING                           // Smooth partial loop
                : AO_VORTEX_TWISTED_RING;                  // Rough partial loop
        } else if (aw < 1.2f) {
            /* |W| < 1.2: Near-complete or full loop */
            out->vortex_class = (k < 0.3f)
                ? AO_VORTEX_LOOP                           // Smooth full loop
                : AO_VORTEX_KNOTTED_LOOP;                  // Rough full loop (knotted)
        } else {
            /* |W| >= 1.2: Multiple loops -- spiral topology */
            out->vortex_class = (k < 0.3f)
                ? AO_VORTEX_SPIRAL                         // Smooth spiral
                : AO_VORTEX_KNOTTED_SPIRAL;                // Rough spiral (knotted)
        }
    }
}

/* ╔══════════════════════════════════════════════════════════════════════════╗
 * ║                                                                        ║
 * ║  SECTION 7: COHERENCE FIELD (Cross-Modal Coherence Composite)          ║
 * ║                                                                        ║
 * ║  Maintains 4 coherence streams from different input modalities:        ║
 * ║    - HEARTBEAT (0.4): CK's internal rhythm, most trustworthy          ║
 * ║    - TEXT      (0.3): Coherence derived from text comprehension        ║
 * ║    - AUDIO     (0.2): Coherence from audio/sound input                ║
 * ║    - NARRATIVE  (0.1): Coherence from narrative arc detection          ║
 * ║                                                                        ║
 * ║  The unified coherence is the weighted average across all streams.     ║
 * ║  This feeds into the coherence gates as the "field_coh" parameter.     ║
 * ║                                                                        ║
 * ║  WHY weighted streams: Different modalities have different             ║
 * ║  reliability and latency. The heartbeat is always present and          ║
 * ║  internally generated (most trustworthy = highest weight).             ║
 * ║  Text is the primary external input. Audio and narrative are           ║
 * ║  supplementary signals with lower confidence.                          ║
 * ║                                                                        ║
 * ║  WHY normalized (divide by wsum): If weights don't sum to 1.0,        ║
 * ║  the normalization ensures the unified value stays in [0, 1].          ║
 * ║  Currently weights sum to 1.0, but normalization future-proofs         ║
 * ║  against weight changes.                                               ║
 * ║                                                                        ║
 * ╚══════════════════════════════════════════════════════════════════════════╝ */

/*
 * ao_field_init -- Initialize the coherence field to default weights.
 *
 * Sets all stream values to 0.0 (no coherence measured yet) and
 * establishes the default weight distribution:
 *   Heartbeat: 0.4 (internal, always present, most reliable)
 *   Text:      0.3 (primary external input)
 *   Audio:     0.2 (supplementary external input)
 *   Narrative: 0.1 (high-level pattern, most uncertain)
 */
void ao_field_init(AO_CoherenceField* f)
{
    memset(f, 0, sizeof(*f));
    f->weights[AO_STREAM_HEARTBEAT] = 0.4f;   // Heartbeat: internal rhythm, most trusted
    f->weights[AO_STREAM_TEXT]      = 0.3f;   // Text: primary external signal
    f->weights[AO_STREAM_AUDIO]     = 0.2f;   // Audio: supplementary external
    f->weights[AO_STREAM_NARRATIVE] = 0.1f;   // Narrative: high-level arc, least certain
}

/*
 * ao_field_update -- Update a single stream and recompute unified coherence.
 *
 * WHAT: Sets the coherence value for one stream, then recalculates the
 *       weighted average across all streams.
 *
 * HOW:
 *   1. Store the new value for the specified stream
 *   2. Compute unified = sum(weight_i * stream_i) / sum(weight_i)
 *
 * WHY recompute on every update: The unified coherence must always
 * reflect the latest state of all streams. Since updates arrive
 * asynchronously (heartbeat at 50Hz, text when typed, audio when
 * heard), we recompute the full weighted average each time.
 */
void ao_field_update(AO_CoherenceField* f, int stream_id, float value)
{
    float sum, wsum;
    int i;

    if (stream_id >= 0 && stream_id < AO_NUM_STREAMS)
        f->streams[stream_id] = value;

    /* Recompute unified coherence as weighted average */
    sum = 0.0f;
    wsum = 0.0f;
    for (i = 0; i < AO_NUM_STREAMS; i++) {
        sum  += f->weights[i] * f->streams[i]; // Weighted contribution
        wsum += f->weights[i];                  // Total weight (for normalization)
    }
    f->unified = (wsum > 0.0f) ? sum / wsum : 0.0f; // Normalized weighted average
}

/*
 * ao_field_unified -- Read the current unified coherence value.
 *
 * Returns the most recently computed weighted average of all streams.
 * This is the "field_coh" value that feeds into ao_gate_measure()
 * as the external coherence component (40% of raw gate input).
 */
float ao_field_unified(const AO_CoherenceField* f)
{
    return f->unified;
}
