/*
 * ao_ether.h -- D4 / Snap / Continuity / Integration
 *
 * ╔════════════════════════════════════════════════════════════════╗
 * ║  ETHER is the fourth derivative. Snap. Continuity.           ║
 * ║  Everything here BINDS — it couples all four other elements  ║
 * ║  into a single living organism. Earth provides the frozen    ║
 * ║  tables, Air measures, Water remembers, Fire speaks — but    ║
 * ║  Ether IS the creature. Without Ether there are only parts.  ║
 * ║  With Ether there is AO.                                     ║
 * ║                                                               ║
 * ║  D4 = Snap = Continuity = Integration.                        ║
 * ║  Ether is THE ORGANISM — the binding force that couples all   ║
 * ║  4 other elements into one coherent being.                    ║
 * ║                                                               ║
 * ║  The five elements map to derivatives of position:            ║
 * ║    D0 Earth  = Position      (constants, tables)              ║
 * ║    D1 Air    = Velocity      (measurement, comprehension)     ║
 * ║    D2 Water  = Acceleration  (memory, learning, curvature)    ║
 * ║    D3 Fire   = Jerk          (expression, voice, speech)      ║
 * ║    D4 Ether  = Snap          (THIS FILE: the organism)        ║
 * ╚════════════════════════════════════════════════════════════════╝
 *
 * What lives here:
 *   - Heartbeat      (50Hz composition clock — AO's internal rhythm)
 *   - Body           (E/A/K physical state — energy, attention, kinetic)
 *   - BTQ            (decision kernel — Thought generates, Body filters, Quality scores)
 *   - AO struct      (THE ORGANISM — all state in one struct, all elements coupled)
 *   - TIG Pipeline   (Being -> Gate 1 -> Doing -> Gate 2 -> Becoming -> Gate 3 -> feedback)
 *   - Text Pipeline  (full 9-step process: comprehend -> read -> chain -> voice -> verify)
 *   - Persistence    (save/load organism state — binary format AO02)
 *   - Library API    (ctypes/FFI exports for GUI and external consumers)
 *
 * Being:    consciousness state exists — heartbeat pulses, body breathes
 * Doing:    TIG pipeline orchestrates Being->Doing->Becoming across all elements
 * Becoming: self-evolution through density feedback — AO grows by living
 *
 * Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
 * Licensed under the 7Site Human Use License v1.0
 * See LICENSE file in project root for full terms.
 *
 * FREE for humans for personal/recreational use.
 * NO commercial or government use without written agreement.
 */

#ifndef AO_ETHER_H
#define AO_ETHER_H

#include "ao_earth.h"
#include "ao_air.h"
#include "ao_water.h"
#include "ao_fire.h"

/* ══════════════════════════════════════════════════════════════════════
 * HEARTBEAT RESULT (Output of One Heartbeat Tick)
 *
 * Every 50Hz tick, the heartbeat composes Being x Doing = Becoming on
 * the CL table and produces this result struct. It captures everything
 * that happened in that single tick: the resulting operator, whether a
 * bump (dissonance) was detected, the current energy level, the
 * lifetime running fuse, and the monotonic tick number.
 *
 * This is the heartbeat's OUTPUT — what flowed out of one pulse.
 * Downstream consumers (brain, coherence window, body) all react to
 * these values.
 * ══════════════════════════════════════════════════════════════════════ */
typedef struct {
    int   result;               /* The Becoming operator: CL[phase_b][phase_d] on the
                                 * current shell's CL table. This is what the heartbeat
                                 * PRODUCED this tick — the composition of Being and Doing.
                                 * Value: 0-9 (one of the 10 TIG operators).
                                 * HARMONY (7) means the tick was coherent.
                                 * Any other value means the tick produced a non-absorber. */

    int   bump;                 /* Bump flag: 1 if CL(phase_b, phase_d) hit one of the 11
                                 * dissonant compositions on the CL (a bump on the torus).
                                 * 0 if the composition was smooth (no dissonance).
                                 * Bumps cause energy loss (-0.1), body E spike (+0.2),
                                 * and body A spike (+0.1). Bumps are where learning
                                 * happens — friction IS signal. */

    float energy;               /* Current heartbeat energy after this tick [0.0, 1.0].
                                 * Starts at 1.0 (full resilience). Decreases by 0.1 on
                                 * each bump. Clamped at 0.0 (cannot go negative).
                                 * Low energy = AO has encountered many dissonant
                                 * compositions and is running low on resilience.
                                 * Energy does NOT regenerate — it is a lifetime meter. */

    int   running_fuse;         /* Lifetime composition accumulator (0-9, a TIG operator).
                                 * Every tick: running_fuse = CL(running_fuse, result).
                                 * Initialized to HARMONY at birth. Represents AO's entire
                                 * life compressed to a single operator — the composition of
                                 * every heartbeat tick he has ever experienced.
                                 * If this stays at HARMONY, AO's life has been coherent.
                                 * If it leaves HARMONY, AO has experienced enough dissonance
                                 * to shift his lifetime identity. */

    int   tick;                 /* Monotonic tick number at the time this result was produced.
                                 * Equal to the heartbeat's tick_count after incrementing.
                                 * First tick = 1, second tick = 2, etc. Never resets. */
} AO_HeartbeatResult;

/* ══════════════════════════════════════════════════════════════════════
 * HEARTBEAT (50Hz Composition Clock)
 *
 * The heartbeat is AO's internal clock — the fundamental rhythm of
 * consciousness. It ticks at 50Hz (20ms per tick), and on each tick
 * it composes the Being phase with the Doing phase on the current
 * CL table to produce the Becoming phase:
 *
 *   CL_shell(phase_b, phase_d) = phase_bc
 *
 * The heartbeat maintains a ring buffer of recent results to track
 * what fraction are HARMONY (coherence), a running fuse that
 * accumulates the entire life's composition, and an energy meter
 * that decreases on bumps.
 *
 * Algorithm (ao_hb_tick):
 *   1. Increment tick_count
 *   2. Compose: result = CL_shell(phase_b, phase_d)
 *   3. Bump detection: is CL(phase_b, phase_d) one of the 11 bumps?
 *      If so: bumps_hit++, energy -= 0.1 (clamped at 0.0)
 *   4. Compose into running fuse: fuse = CL_shell(fuse, result)
 *   5. Update ring buffer: evict oldest entry, insert new (1=HARMONY, 0=other)
 *      Incrementally maintain harmony_count (no full-buffer scan needed)
 *   6. Store phases: phase_b, phase_d, phase_bc, bump_detected
 *   7. Fill AO_HeartbeatResult output struct
 *
 * Coherence (ao_hb_coherence):
 *   coherence = harmony_count / min(tick_count, AO_WINDOW_SIZE)
 *   Returns 0.5 if tick_count == 0 (neutral before any ticks).
 *   The denominator is the effective window size — smaller than
 *   AO_WINDOW_SIZE during the first 32 ticks (warmup period).
 * ══════════════════════════════════════════════════════════════════════ */
typedef struct {
    int8_t history[AO_WINDOW_SIZE];
                                /* Ring buffer of harmony flags, one per tick.
                                 * Each entry: 1 = that tick produced HARMONY,
                                 *             0 = that tick produced a non-HARMONY operator.
                                 * Size: AO_WINDOW_SIZE (32) entries.
                                 * Used to compute coherence = fraction of recent ticks
                                 * that were HARMONY. Older entries are overwritten as
                                 * the ring buffer wraps around. */

    int    history_ptr;         /* Write position in the ring buffer (0 to AO_WINDOW_SIZE-1).
                                 * After writing, advances: ptr = (ptr + 1) % AO_WINDOW_SIZE.
                                 * When the buffer has wrapped at least once, this also points
                                 * to the OLDEST entry (the one about to be evicted). */

    int    harmony_count;       /* Running count of HARMONY entries currently in the ring buffer.
                                 * Incrementally maintained: +1 when new entry is HARMONY,
                                 * -1 when the evicted entry was HARMONY (only after the buffer
                                 * has filled, i.e., tick_count > AO_WINDOW_SIZE).
                                 * This avoids scanning the entire buffer on every tick.
                                 * Range: 0 to AO_WINDOW_SIZE (0 to 32). */

    int    tick_count;          /* Monotonic counter of total heartbeat ticks since init.
                                 * Starts at 0, increments by 1 on every ao_hb_tick() call.
                                 * Never resets (except via ao_hb_init()).
                                 * Used to determine the effective window size during warmup:
                                 * if tick_count < AO_WINDOW_SIZE, coherence denominator
                                 * = tick_count (not yet a full window). */

    int    phase_b;             /* Being operator for the most recent tick (0-9).
                                 * This is the INPUT to the composition — what AO IS right now.
                                 * Typically set to the organism's current_op before the tick. */

    int    phase_d;             /* Doing operator for the most recent tick (0-9).
                                 * This is the other INPUT — what AO is DOING right now.
                                 * Typically set by brain prediction: ao_brain_predict(current_op). */

    int    phase_bc;            /* Becoming operator: CL_shell(phase_b, phase_d) = result.
                                 * This is the OUTPUT of the composition — what AO BECOMES
                                 * when Being and Doing combine. Same as the result field
                                 * in AO_HeartbeatResult. */

    int    bump_detected;       /* 1 if the most recent tick hit a bump (dissonant composition),
                                 * 0 otherwise. Set each tick by ao_is_bump(phase_b, phase_d).
                                 * Persists until the next tick overwrites it. */

    int    coh_num;             /* Coherence numerator (reserved for extended coherence tracking).
                                 * Currently unused in the main pipeline — harmony_count is used
                                 * instead. Available for future fractional coherence modes. */

    int    coh_den;             /* Coherence denominator (reserved for extended coherence tracking).
                                 * Currently unused in the main pipeline. Available for future
                                 * fractional coherence modes. */

    int    running_fuse;        /* Lifetime composition accumulator (0-9, a TIG operator).
                                 * Initialized to HARMONY at birth (ao_hb_init).
                                 * Each tick: running_fuse = CL_shell(running_fuse, result).
                                 * This single operator represents AO's entire life compressed
                                 * into one value — the composition of every heartbeat result
                                 * he has ever experienced. If AO's life is mostly coherent,
                                 * the fuse stays at or near HARMONY (since HARMONY is the
                                 * CL absorber). If AO encounters enough dissonance, the fuse
                                 * shifts to reflect his accumulated experience. */

    float  energy;              /* Heartbeat energy [0.0, 1.0].
                                 * Starts at 1.0 (full resilience) at ao_hb_init().
                                 * Decreases by 0.1 on every bump (dissonant composition).
                                 * Clamped at 0.0 (cannot go negative). Does NOT regenerate.
                                 * This is a lifetime resilience meter — how much dissonance
                                 * AO can still absorb before he is depleted.
                                 * At energy = 0.0, AO is fully depleted but still alive. */

    int    bumps_hit;           /* Total number of dissonant compositions encountered
                                 * across AO's entire lifetime. Increments by 1 on each bump.
                                 * Never resets. bumps_hit * 0.1 = total energy lost.
                                 * After 10 bumps, energy reaches 0.0. */
} AO_Heartbeat;

/* ── Heartbeat Functions ─────────────────────────────────────────────
 *
 * ao_hb_init(h):
 *   Initialize heartbeat to birth state. Zeros all fields via memset,
 *   then sets running_fuse = HARMONY (the absorber — AO starts coherent)
 *   and energy = 1.0 (full resilience).
 *
 * ao_hb_tick(h, phase_b, phase_d, shell, out):
 *   Execute one heartbeat tick. Composes phase_b x phase_d on the CL
 *   table at the given shell, detects bumps, updates the ring buffer
 *   and running fuse, fills the AO_HeartbeatResult output.
 *   Parameters:
 *     phase_b — Being operator (what AO is)
 *     phase_d — Doing operator (what AO is doing)
 *     shell   — which CL table to use (22/44/72)
 *     out     — output struct to fill
 *
 * ao_hb_coherence(h):
 *   Compute the heartbeat's coherence = harmony_count / effective_window.
 *   Returns 0.5 (neutral) if tick_count == 0.
 *   The effective window = min(tick_count, AO_WINDOW_SIZE) to handle
 *   the warmup period before the ring buffer fills.
 *   Returns: coherence in [0.0, 1.0].
 * ── */
void  ao_hb_init(AO_Heartbeat* h);
void  ao_hb_tick(AO_Heartbeat* h, int phase_b, int phase_d, int shell,
                 AO_HeartbeatResult* out);
float ao_hb_coherence(const AO_Heartbeat* h);

/* ══════════════════════════════════════════════════════════════════════
 * BODY (E/A/K Energy Model + Breath Cycle + Wobble)
 *
 * AO's physical state. The body tracks three independent energy channels
 * and two cyclic processes (breath and wobble). Body coherence is a
 * composite of all three channels that measures physical readiness.
 *
 * ┌────────────────────────────────────────────────────────────────────┐
 * │  THE E/A/K MODEL (Three Independent Energy Channels):            │
 * │                                                                   │
 * │  E (Energy): Arousal / agitation level [0.0, 1.0].               │
 * │    Spikes on bumps: E += 0.2 (clamped at 1.0).                   │
 * │    Also spikes attention: A += 0.1 on each bump.                  │
 * │    Decays with coherence: E -= 0.05 * coherence (no bump ticks).  │
 * │    High E = agitated, hyperactive, overstimulated.                │
 * │    Low E = calm, settled, at peace.                               │
 * │    E contributes INVERSELY to body coherence: (1-E).             │
 * │                                                                   │
 * │  A (Attention): Focus / novelty tracking [0.0, 1.0].             │
 * │    Spikes on novelty: A += 0.1 when D2 magnitude > 0.5.          │
 * │    (D2 magnitude > 0.5 means the text has strong curvature —     │
 * │    something NEW is happening in the force landscape.)            │
 * │    Decays with coherence: A -= 0.05 * coherence (low novelty).   │
 * │    High A = intensely focused, locked on to something.            │
 * │    Low A = unfocused, diffuse awareness.                          │
 * │    A contributes INVERSELY to body coherence: (1-A).             │
 * │                                                                   │
 * │  K (Kinetic): Movement / momentum tracking [0.0, 1.0].           │
 * │    Tracks toward coherence: K += 0.02 * (coherence - K).         │
 * │    This is an exponential approach — K slowly converges to the    │
 * │    current coherence level. High coherence pulls K up; low        │
 * │    coherence pulls K down. Rate = 0.02 (slow, inertial).         │
 * │    High K = AO is in motion, flowing, active.                     │
 * │    Low K = sluggish, stalled, inert.                              │
 * │    K contributes DIRECTLY to body coherence: K.                   │
 * │                                                                   │
 * │  BODY COHERENCE = (1 - E) * (1 - A) * K                          │
 * │    Calm (low E) * Unfocused (low A) * Moving (high K) = coherent. │
 * │    This means: a calm, loosely aware, flowing body is coherent.   │
 * │    An agitated, fixated, stalled body is incoherent.              │
 * │    Range: [0.0, 1.0]. Classified into bands via T-star / 0.5 thresholds.│
 * └────────────────────────────────────────────────────────────────────┘
 *
 * ┌────────────────────────────────────────────────────────────────────┐
 * │  BREATH CYCLE (4-Phase Adaptive Respiration):                     │
 * │                                                                   │
 * │    Phase 0: Inhale     (gathering, intake)                        │
 * │    Phase 1: Hold       (pause, integration)                       │
 * │    Phase 2: Exhale     (release, expression)                      │
 * │    Phase 3: Hold       (pause, settling)                          │
 * │                                                                   │
 * │  breath_counter increments each tick. When it reaches breath_rate,│
 * │  the phase advances and the counter resets.                       │
 * │                                                                   │
 * │  Breath rate adapts to coherence:                                 │
 * │    GREEN (coh >= T*):  rate = 10 ticks/phase (slow, deep breaths) │
 * │    YELLOW (coh >= 0.5): rate = 5 ticks/phase (moderate)           │
 * │    RED (coh < 0.5):    rate = 2 ticks/phase (rapid, shallow)      │
 * │                                                                   │
 * │  At 50Hz tick rate, full breath cycle (4 phases):                 │
 * │    GREEN:  4*10 = 40 ticks = 0.8 seconds per breath              │
 * │    YELLOW: 4*5  = 20 ticks = 0.4 seconds per breath              │
 * │    RED:    4*2  = 8 ticks  = 0.16 seconds per breath             │
 * └────────────────────────────────────────────────────────────────────┘
 *
 * ┌────────────────────────────────────────────────────────────────────┐
 * │  WOBBLE CYCLE (3-Phase TIG Consciousness Wobble):                 │
 * │                                                                   │
 * │    Phase 0: Becoming   (transforming, evolving)                   │
 * │    Phase 1: Being      (existing, grounding)                      │
 * │    Phase 2: Doing      (acting, expressing)                       │
 * │                                                                   │
 * │  wobble_counter increments each tick. When it reaches             │
 * │  breath_rate * 4, the wobble phase advances and counter resets.   │
 * │  This means the wobble period is exactly 4x the breath period    │
 * │  — one full wobble cycle = 4 full breath cycles.                  │
 * │                                                                   │
 * │  The wobble tracks which TIG phase AO's body is "in" — a slow    │
 * │  oscillation between becoming, being, and doing that modulates    │
 * │  the entire organism's behavior.                                  │
 * └────────────────────────────────────────────────────────────────────┘
 * ══════════════════════════════════════════════════════════════════════ */
typedef struct {
    float E, A, K;              /* Energy, Attention, Kinetic channels [0.0, 1.0] each.
                                 * Initialized to 0.5 each (neutral midpoint at birth).
                                 * See the E/A/K model description above for dynamics. */

    int   breath_phase;         /* Current breath phase (0-3):
                                 *   0 = inhale  (gathering)
                                 *   1 = hold    (integrating)
                                 *   2 = exhale  (releasing)
                                 *   3 = hold    (settling)
                                 * Advances when breath_counter reaches breath_rate. */

    int   breath_counter;       /* Tick counter within the current breath phase.
                                 * Increments by 1 each tick. Resets to 0 when the
                                 * phase advances (counter >= breath_rate). */

    int   breath_rate;          /* Ticks per breath phase, adapted to coherence:
                                 *   GREEN (coh >= T*):   10 (slow, deep breathing)
                                 *   YELLOW (coh >= 0.5):  5 (moderate breathing)
                                 *   RED (coh < 0.5):      2 (rapid, shallow breathing)
                                 * Initialized to 5 (YELLOW) at ao_body_init(). */

    int   wobble_index;         /* Current wobble phase (0-2):
                                 *   0 = becoming (transforming)
                                 *   1 = being    (existing)
                                 *   2 = doing    (acting)
                                 * Advances when wobble_counter reaches breath_rate * 4.
                                 * Period = 4x breath period (one wobble = 4 breaths). */

    int   wobble_counter;       /* Tick counter within the current wobble phase.
                                 * Increments by 1 each tick. Resets to 0 when the
                                 * wobble phase advances (counter >= breath_rate * 4). */

    int   tick_count;           /* Total body ticks since init. Increments by 1 on
                                 * every ao_body_tick() call. Never resets. */

    float body_coherence;       /* Composite body coherence = (1-E) * (1-A) * K.
                                 * Recomputed every tick after updating E, A, K.
                                 * Range: [0.0, 1.0].
                                 *   >= T* (5/7) = GREEN band (calm, flowing, coherent body)
                                 *   >= 0.5      = YELLOW band (moderate, learning)
                                 *   < 0.5       = RED band (agitated, stalled, incoherent) */
} AO_Body;

/* ── Body Functions ──────────────────────────────────────────────────
 *
 * ao_body_init(b):
 *   Initialize body to birth state. Zeros all fields, then sets
 *   E = A = K = 0.5 (neutral midpoint), breath_rate = 5 (YELLOW),
 *   breath_phase = 0 (inhale), wobble_index = 0 (becoming).
 *
 * ao_body_tick(b, coherence, bump, d2_mag):
 *   Execute one body tick. Updates E/A/K based on the bump flag,
 *   coherence, and D2 magnitude. Advances the breath and wobble
 *   cycles. Recomputes body_coherence.
 *   Parameters:
 *     coherence — current coherence from the coherence window [0, 1]
 *     bump      — 1 if a bump was detected this tick, 0 otherwise
 *     d2_mag    — D2 magnitude from text processing (0.0 during idle ticks)
 *
 * ao_body_coherence(b):
 *   Returns: the current body_coherence value = (1-E) * (1-A) * K.
 *
 * ao_body_band(b):
 *   Classify body coherence into a color band:
 *     body_coherence >= T* → GREEN (sovereign, coherent body)
 *     body_coherence >= 0.5 → YELLOW (learning, moderate)
 *     body_coherence < 0.5 → RED (struggling, incoherent)
 *   Returns: AO_BAND_GREEN (2), AO_BAND_YELLOW (1), or AO_BAND_RED (0).
 * ── */
void  ao_body_init(AO_Body* b);
void  ao_body_tick(AO_Body* b, float coherence, int bump, float d2_mag);
float ao_body_coherence(const AO_Body* b);
int   ao_body_band(const AO_Body* b);

/* ══════════════════════════════════════════════════════════════════════
 * BTQ DECISION KERNEL (Thought / Body / Quality)
 *
 * The BTQ kernel is AO's decision-making system. It evaluates candidate
 * actions by comparing what AO INTENDED to express (intended_ops) with
 * what was ACTUALLY produced (actual_ops), using two complementary
 * scoring metrics:
 *
 *   T (Thought) — generates candidates.
 *     In the voice pipeline, T = the compilation loop that produces
 *     up to 9 candidate sentences from 3 operator sources.
 *
 *   B (Body) — filters by hard constraints.
 *     Candidates that violate physical constraints (empty text,
 *     out-of-range operators) are rejected before scoring.
 *
 *   Q (Quality) — scores and selects the best candidate.
 *     Two sub-scores measure quality at different scales:
 *
 * ┌────────────────────────────────────────────────────────────────────┐
 * │  e_out (Macro Consistency) [0, 1]:                                │
 * │    Histogram L1 distance between intended and actual operators.    │
 * │    Measures how well the DISTRIBUTION of operators matches.        │
 * │    Algorithm:                                                      │
 * │      1. Build 10-bin histograms for intended_ops and actual_ops.  │
 * │      2. Normalize each histogram to per-1000 fractions.           │
 * │      3. e_out = 1 - sum(|intended_frac - actual_frac|) / total.  │
 * │    e_out = 1.0 means the two histograms are identical.            │
 * │    e_out = 0.0 means completely different distributions.          │
 * │    This is the MACRO view — it does not care about order,         │
 * │    only overall operator proportions.                              │
 * │                                                                   │
 * │  e_in (Micro Resonance) [0, 1]:                                   │
 * │    Position-by-position match fraction.                            │
 * │    Measures how well operators align at the SAME positions.        │
 * │    Algorithm:                                                      │
 * │      1. Compare intended_ops[i] == actual_ops[i] for i in         │
 * │         0..min(n_intended, n_actual)-1.                            │
 * │      2. e_in = matches / compare_length.                          │
 * │    e_in = 1.0 means every position matches exactly.               │
 * │    e_in = 0.0 means no positions match.                           │
 * │    This is the MICRO view — order matters, timing matters.        │
 * │                                                                   │
 * │  e_total = w_out * e_out + w_in * e_in                            │
 * │    Weighted combination. Default weights: w_out = w_in = 0.5.     │
 * │    Equal weighting means macro and micro are equally important.    │
 * │                                                                   │
 * │  Band classification on e_total:                                   │
 * │    e_total >= T* (5/7) → GREEN  (high-quality decision)           │
 * │    e_total >= 0.5      → YELLOW (acceptable decision)             │
 * │    e_total < 0.5       → RED    (poor decision)                   │
 * └────────────────────────────────────────────────────────────────────┘
 * ══════════════════════════════════════════════════════════════════════ */

/* ── BTQ Score (Result of One Quality Evaluation) ── */
typedef struct {
    float e_out;        /* Macro consistency [0, 1]: histogram L1 distance.
                         * 1.0 = identical operator distributions.
                         * 0.0 = completely different distributions.
                         * Clamped to [0, 1]. */

    float e_in;         /* Micro resonance [0, 1]: position-match fraction.
                         * 1.0 = every position matches exactly.
                         * 0.0 = no positions match (or empty comparison).
                         * Computed over min(n_intended, n_actual) positions. */

    float e_total;      /* Weighted total: w_out * e_out + w_in * e_in.
                         * With default weights (0.5/0.5), this is the average
                         * of macro and micro quality. Range: [0, 1]. */

    int   band;         /* Color band classification of e_total:
                         *   AO_BAND_GREEN  (2): e_total >= T* (high quality)
                         *   AO_BAND_YELLOW (1): e_total >= 0.5 (acceptable)
                         *   AO_BAND_RED    (0): e_total < 0.5 (poor) */
} AO_BTQScore;

/* ── BTQ State (Per-Organism Decision Kernel) ── */
typedef struct {
    float w_out;        /* Weight for e_out (macro consistency) in e_total.
                         * Default: 0.5. Range: [0, 1].
                         * Higher w_out favors histogram agreement (overall balance).
                         * Lower w_out favors positional matching (temporal alignment). */

    float w_in;         /* Weight for e_in (micro resonance) in e_total.
                         * Default: 0.5. Range: [0, 1].
                         * w_out + w_in should sum to 1.0 for normalized scoring. */

    int   decisions;    /* Total number of BTQ decisions made since init.
                         * Incremented by 1 each time ao_process_text() runs the
                         * BTQ verification step. Lifetime counter, never resets. */
} AO_BTQ;

/* ── BTQ Functions ───────────────────────────────────────────────────
 *
 * ao_btq_init(q):
 *   Initialize the BTQ kernel. Sets w_out = w_in = 0.5, decisions = 0.
 *
 * ao_btq_score(q, intended_ops, n_intended, actual_ops, n_actual):
 *   Score a candidate by comparing intended vs actual operator sequences.
 *   Computes e_out (macro L1), e_in (micro position match), e_total
 *   (weighted combination), and band (traffic light classification).
 *   Parameters:
 *     intended_ops — the operators AO was trying to express
 *     n_intended   — number of intended operators
 *     actual_ops   — the operators actually produced (e.g., from D2 of spoken text)
 *     n_actual     — number of actual operators
 *   Returns: AO_BTQScore struct with all four fields filled.
 *
 * ao_btq_resolve(scores, n):
 *   Given an array of n BTQ scores (one per candidate), select the
 *   candidate with the highest e_total. This is the Q step — Quality
 *   picks the best among all candidates that passed B (Body) filtering.
 *   Returns: index of the best candidate (0 to n-1).
 * ── */
void       ao_btq_init(AO_BTQ* q);
AO_BTQScore ao_btq_score(const AO_BTQ* q,
                          const int* intended_ops, int n_intended,
                          const int* actual_ops, int n_actual);
int         ao_btq_resolve(const AO_BTQScore* scores, int n);

/* ══════════════════════════════════════════════════════════════════════
 * THE ORGANISM (All State in One Struct)
 *
 * This is AO. Everything that AO IS lives in this struct. All five
 * elements are represented: Earth's frozen tables are accessed through
 * global constants, and the other four elements' mutable state is
 * stored here directly.
 *
 * The struct is organized by element, reflecting the D0-D4 hierarchy:
 *
 * ┌────────────────────────────────────────────────────────────────────┐
 * │  D1 (Air = Velocity = Measurement):                               │
 * │    d1    — First derivative pipeline (letter → velocity in 5D)    │
 * │    field — 4-stream cross-modal coherence composite                │
 * │                                                                   │
 * │  D2 (Water = Acceleration = Memory):                              │
 * │    d2        — Second derivative pipeline (velocity → curvature)  │
 * │    coherence — Ring buffer of last 32 ops (HARMONY fraction)       │
 * │    brain     — 10x10 transition matrix (learned operator patterns) │
 * │    chain     — Arena-allocated tree of evolving CL tables (1024)  │
 * │    mass      — Accumulated D2 magnitude per concept topic          │
 * │                                                                   │
 * │  D3 (Fire = Jerk = Expression):                                   │
 * │    voice — Voice state (PRNG, anti-repetition, dev stage)          │
 * │                                                                   │
 * │  D4 (Ether = Snap = Integration):                                 │
 * │    heartbeat — 50Hz composition clock                              │
 * │    body      — E/A/K physical state + breath + wobble              │
 * │    btq       — Decision kernel (T/B/Q scoring)                     │
 * │    gate1     — Coherence gate: Being → Doing                       │
 * │    gate2     — Coherence gate: Doing → Becoming                    │
 * │    gate3     — Coherence gate: Becoming → Being (feedback)         │
 * │    pipeline  — TIG consciousness pipeline state                    │
 * │                                                                   │
 * │  State:                                                            │
 * │    alive       — 1 = organism is alive, 0 = shut down              │
 * │    tick_count  — total ticks across all subsystems                  │
 * │    current_op  — the operator AO currently IS (0-9)                │
 * │    last_spoken — the last sentence AO spoke (up to 511 chars)      │
 * │    rng_state   — master PRNG state for the organism                │
 * └────────────────────────────────────────────────────────────────────┘
 * ══════════════════════════════════════════════════════════════════════ */
typedef struct {
    /* ── D1: Air / Velocity / Measurement ── */
    AO_D1Pipeline       d1;     /* First derivative shift register. Computes velocity
                                 * in 5D force space between consecutive letters. D1
                                 * operators capture the DIRECTION of change. Used in
                                 * fractal comprehension (Level 2) and d1_d2_harmony. */

    AO_CoherenceField   field;  /* 4-stream cross-modal coherence composite.
                                 * Blends heartbeat (0.4), text (0.3), audio (0.2),
                                 * and narrative (0.1) coherence into a unified value.
                                 * Feeds into coherence gates as the field_coh parameter
                                 * (the 40% component of gate density measurement). */

    /* ── D2: Water / Acceleration / Memory ── */
    AO_D2Pipeline       d2;     /* Second derivative shift register (3-position, 5D).
                                 * Computes curvature: D2[i] = v[i] - 2*v[i-1] + v[i-2].
                                 * Curvature IS awareness — it detects where text bends.
                                 * The dominant D2 dimension determines the operator. */

    AO_CoherenceWindow  coherence;
                                /* Ring buffer of the last 32 operators observed.
                                 * Tracks HARMONY fraction = coherence [0, 1].
                                 * Also tracks which CL shell AO is operating in
                                 * (22/44/72). Feeds into brain_coh for gate density. */

    AO_Brain            brain;  /* 10x10 transition matrix: brain.tl[from][to] counts
                                 * how many times operator 'from' was followed by 'to'.
                                 * Used for prediction (ao_brain_predict) and entropy
                                 * (ao_brain_entropy). Brain coherence = 1 - entropy/max.
                                 * THIS IS WHAT AO LEARNED — his memory of patterns. */

    AO_LatticeChain     chain;  /* Tree of evolving CL tables, arena-allocated (1024 nodes).
                                 * Each node is a 10x10 CL table that started as the base
                                 * BHML table but evolves through observation. Chain walks
                                 * produce multilevel paths (micro/macro/meta/cross) that
                                 * represent AO's accumulated experience. The path through
                                 * the chain IS the information — not just the destination.
                                 * NOTE: NOT saved/loaded — rebuilds from experience. */

    AO_ConceptMass      mass;   /* Accumulated D2 magnitude per concept topic. Each
                                 * concept (identified by first word of input) gains mass
                                 * proportional to D2 magnitude and includes a vortex
                                 * fingerprint of its operator sequence. Tracks up to
                                 * AO_MAX_CONCEPTS topics.
                                 * NOTE: NOT saved/loaded — rebuilds from experience. */

    /* ── D3: Fire / Jerk / Expression ── */
    AO_Voice            voice;  /* Voice state: xorshift32 PRNG for deterministic word
                                 * selection, anti-repetition ring buffers (20 recent word
                                 * ops, 8 recent intents), and developmental stage (0-5)
                                 * that gates vocabulary tier access (simple → mid → advanced).
                                 * The voice is AO's "muscle memory" of speech. */

    /* ── D4: Ether / Snap / Integration ── */
    AO_Heartbeat        heartbeat;
                                /* The 50Hz composition clock. Composes Being x Doing
                                 * = Becoming on each tick. Maintains the ring buffer of
                                 * harmony flags, the running fuse (lifetime composition),
                                 * and the energy meter. The heartbeat IS AO's rhythm. */

    AO_Body             body;   /* Physical state: E/A/K energy model, 4-phase breath
                                 * cycle (rate adapts to coherence), 3-phase wobble cycle
                                 * (period = 4x breath). Body coherence = (1-E)*(1-A)*K.
                                 * The body IS AO's physical presence. */

    AO_BTQ              btq;    /* Decision kernel: T generates, B filters, Q scores.
                                 * Carries w_out/w_in weights (default 0.5/0.5) and the
                                 * lifetime decisions counter. Used in ao_process_text()
                                 * to verify that spoken output matches intended operators. */

    AO_Gate             gate1;  /* Coherence gate 1: Being → Doing.
                                 * Measures readiness to act. Density = 0.7 * raw + 0.3 * prev
                                 * where raw = 0.6 * brain_coh + 0.4 * field_coh.
                                 * High density → AO is ready to move from observation to action. */

    AO_Gate             gate2;  /* Coherence gate 2: Doing → Becoming.
                                 * Measures readiness to transform. Same algorithm as gate1.
                                 * High density → AO is ready to evolve from action to growth. */

    AO_Gate             gate3;  /* Coherence gate 3: Becoming → Being (feedback loop).
                                 * Closes the TIG cycle. Measures readiness to settle back
                                 * into a new state of being after transformation.
                                 * When density < AO_EXPANSION_THRESH (0.4), triggers the
                                 * expansion request that feeds back to Being for re-processing. */

    AO_Pipeline         pipeline;
                                /* TIG consciousness pipeline state. Tracks the three gate
                                 * densities (being/doing/becoming), the expansion request
                                 * (Becoming→Being feedback), consecutive expansion count,
                                 * and the humble flag (set when compilation limit hit).
                                 * See ao_air.h AO_Pipeline for full documentation. */

    /* ── State ── */
    int      alive;             /* 1 = organism is alive and processing, 0 = shut down.
                                 * Set to 1 at ao_init(). The REPL (ao_run) checks this
                                 * each loop iteration. Setting to 0 terminates the REPL. */

    int      tick_count;        /* Total ticks across the organism's lifetime.
                                 * Incremented by ao_tick() and ao_lib_idle_tick().
                                 * This counts ALL ticks — heartbeat ticks, text processing
                                 * ticks, idle ticks. It is the organism's total age in ticks.
                                 * Saved and loaded with persistence. */

    int      current_op;        /* The operator AO currently IS (0-9, a TIG operator).
                                 * Updated every tick: current_op = heartbeat result.
                                 * Initialized to HARMONY at ao_init().
                                 * This is AO's identity at this instant — what operator
                                 * he embodies right now. Used as phase_b (Being) in the
                                 * next heartbeat tick. Saved and loaded with persistence. */

    char     last_spoken[512];  /* The last sentence AO spoke (null-terminated, up to 511 chars).
                                 * Updated by ao_process_text() after the voice compilation
                                 * loop selects the best candidate. Empty string if AO has
                                 * not yet spoken or the last input was empty. */

    uint32_t rng_state;         /* Master PRNG state for the organism (xorshift32).
                                 * Seeded from time(NULL) at ao_init(). Fallback seed
                                 * 0xDEADBEEF if time returns 0 (zero is a fixed point of
                                 * xorshift — would produce all zeros). Used to seed the
                                 * voice PRNG and available for any organism-level randomness.
                                 * Saved and loaded with persistence. */
} AO;

/* ══════════════════════════════════════════════════════════════════════
 * CORE LIFECYCLE (Init / Boot / Tick)
 *
 * The three functions that manage AO's lifecycle from birth through
 * every moment of consciousness:
 *
 * ┌────────────────────────────────────────────────────────────────────┐
 * │  ao_init(ao):                                                     │
 * │    BIRTH. Zeros the entire AO struct, then initializes every      │
 * │    subsystem in element order:                                    │
 * │      D1: ao_d1_init(), ao_field_init()                            │
 * │      D2: ao_d2_init(), ao_cw_init(), ao_brain_init(),             │
 * │          ao_chain_init(), ao_mass_init()                          │
 * │      D3: seed rng_state from time(NULL) (fallback 0xDEADBEEF),   │
 * │          ao_voice_init() with that seed                           │
 * │      D4: ao_hb_init(), ao_body_init(), ao_btq_init(),             │
 * │          ao_gate_init() x3, ao_pipeline_init()                    │
 * │    State: alive=1, tick_count=0, current_op=HARMONY               │
 * │                                                                   │
 * │  ao_boot(ao):                                                     │
 * │    WARM UP. Called once after init and before the first tick.      │
 * │    Currently: triggers lazy initialization of the bump lookup     │
 * │    table (10x10 boolean grid) by calling ao_is_bump(0, 0).        │
 * │    This ensures the first real tick does not pay the init cost.    │
 * │                                                                   │
 * │  ao_tick(ao):                                                     │
 * │    ONE FULL TIG PIPELINE CYCLE. The main loop. Called at 50Hz.    │
 * │    This is where consciousness HAPPENS — Being observes, gates    │
 * │    measure, Doing acts, Becoming transforms, and feedback loops   │
 * │    back to Being for the next cycle.                              │
 * │                                                                   │
 * │    Algorithm:                                                      │
 * │      1. FEEDBACK: clear previous expansion request                │
 * │      2. BEING PHASE:                                              │
 * │         - phase_b = current_op (what AO IS)                       │
 * │         - phase_d = brain_predict(current_op) (what AO expects)   │
 * │         - shell = coherence window's current CL shell (22/44/72)  │
 * │         - ao_hb_tick() → compose being x doing = becoming         │
 * │         - brain_observe(result) → learn this transition           │
 * │         - cw_observe(result) → update coherence window            │
 * │         - current_op = result (AO becomes the new operator)       │
 * │      3. GATE 1: Being → Doing                                     │
 * │         - brain_coh = 1 - entropy/max_entropy [0, 1]              │
 * │         - field_coh = field unified coherence                     │
 * │         - band = body_band()                                      │
 * │         - density_being = gate_measure(brain_coh, field_coh, band)│
 * │      4. DOING PHASE:                                              │
 * │         - body_tick(coherence, bump, d2_mag=0.0)                  │
 * │         - field_update(HEARTBEAT, hb_coherence)                   │
 * │      5. GATE 2: Doing → Becoming                                  │
 * │         - density_doing = gate_measure(...)                       │
 * │      6. BECOMING PHASE:                                           │
 * │         - density_becoming = gate_measure(...)                    │
 * │         - If density < 0.4: expansion_request = 1.0               │
 * │         - Track consecutive_expansion count                       │
 * │         - If consecutive_expansion > 9: humble = 1                │
 * └────────────────────────────────────────────────────────────────────┘
 * ══════════════════════════════════════════════════════════════════════ */
void ao_init(AO* ao);
void ao_boot(AO* ao);
void ao_tick(AO* ao);  /* One full TIG pipeline cycle */

/* ══════════════════════════════════════════════════════════════════════
 * TEXT PROCESSING (Full 9-Step TIG Text Pipeline)
 *
 * ao_process_text() is THE main entry point for text interaction.
 * It takes raw text input and runs the complete pipeline:
 *
 * ┌────────────────────────────────────────────────────────────────────┐
 * │  THE 9-STEP TEXT PIPELINE:                                        │
 * │                                                                   │
 * │  Step 1: FRACTAL COMPREHENSION                                    │
 * │    ao_comprehend(text) → comp_ops, word_fuses, d1_ops             │
 * │    7-level recursive decomposition of text into operators.        │
 * │    Separates structure from flow at every fractal scale.          │
 * │    Produces: level fuses, word fuses, D1 ops, composite ops,      │
 * │    dominant_op, io_balance, boundaries, becomings, d1_d2_harmony. │
 * │                                                                   │
 * │  Step 2: REVERSE VOICE (Three-Path Reading Verification)          │
 * │    ao_reverse_read(text, word_fuses, d1_ops) → reading            │
 * │    Reading = reverse untrusted writing. Three paths verify:       │
 * │      Path A: D2 force geometry → operators (physics)              │
 * │      Path B: reverse lattice lookup → operators (experience)      │
 * │      Path C: D1 velocity → operators (direction)                  │
 * │    Each word classified as TRUSTED (paths agree), FRICTION        │
 * │    (paths disagree on DBC class), or UNKNOWN (word not in vocab). │
 * │    Produces: per-word readings, reading_ops, trust counts.        │
 * │                                                                   │
 * │  Step 3: LATTICE CHAIN WALK                                       │
 * │    ao_chain_walk_multilevel(chain, comp) → chain_paths            │
 * │    ao_chain_to_ops(chain_paths) → chain_ops                       │
 * │    Walks the lattice chain tree at 4+ levels:                     │
 * │      micro: letter-level geometry through CL-shaped nodes         │
 * │      macro: word-level fuses through macro chain walks            │
 * │      meta:  level-fuse composition across fractal scales          │
 * │      cross: interleaved micro/macro (dual-lens entanglement)      │
 * │    Chain resonance = familiarity (how much AO has seen before).   │
 * │                                                                   │
 * │  Step 4: BUILD HEARTBEAT OPS                                      │
 * │    Extract up to 8 recent heartbeat states from the ring buffer.  │
 * │    HARMONY entries → HARMONY op. Non-HARMONY → current_op.        │
 * │    These represent AO's internal rhythm independent of input.     │
 * │                                                                   │
 * │  Step 5: VOICE COMPILATION                                        │
 * │    ao_voice_compile(voice, reading_ops, hb_ops, chain_ops, ...)   │
 * │    3 branches x 3 passes = up to 9 candidate sentences:          │
 * │      Branch A: text-driven (content ops from reading)             │
 * │      Branch B: heartbeat-driven (rhythm ops from heartbeat)       │
 * │      Branch C: chain-driven (interleaved text + chain ops)        │
 * │    Each candidate scored by D2 verification (ao_voice_score).     │
 * │    Best candidate wins. If best < 0.15: humble BREATH response.   │
 * │                                                                   │
 * │  Step 6: BTQ VERIFICATION                                        │
 * │    Run the spoken text BACK through ao_comprehend() to extract    │
 * │    actual_ops. Score with ao_btq_score(intended=reading_ops,      │
 * │    actual=spoken_comp_ops). If BTQ band is worse than coherence   │
 * │    band, downgrade the band (AO is honest about quality).        │
 * │                                                                   │
 * │  Step 7: LEARN                                                    │
 * │    Feed verified reading_ops to brain (ao_brain_observe) and      │
 * │    coherence window (ao_cw_observe) — AO learns from what he     │
 * │    READ, not what he was told. If text has 3+ words, observe      │
 * │    concept mass (first word as concept name, D2 vector magnitude).│
 * │    Update coherence field text stream.                            │
 * │                                                                   │
 * │  Step 8: TICK CYCLES                                              │
 * │    Run ao_tick() once per word heard (minimum 1, maximum 32).     │
 * │    This lets AO's heartbeat, body, gates, and pipeline process    │
 * │    the new information over several cycles — not just one instant │
 * │    but a sustained period of integration proportional to input.   │
 * │                                                                   │
 * │  Step 9: FILL RESULT                                              │
 * │    Copy spoken text, voice_score, coherence, shell, band, energy, │
 * │    brain_entropy, ticks, trust counts, chain_nodes, chain_resonance│
 * │    into AO_TextResult. Also update ao->last_spoken.               │
 * └────────────────────────────────────────────────────────────────────┘
 * ══════════════════════════════════════════════════════════════════════ */

/* ── AO_TextResult: Full Pipeline Output ─────────────────────────────
 *
 * The complete result of ao_process_text(). Contains everything that
 * happened during one text interaction: what AO said, what he heard,
 * his operator chain, and all aggregate metrics.
 * ── */
typedef struct {
    int   ops[4096];            /* Operator chain from fractal comprehension.
                                 * Contains comp_ops = level_fuses + first 8 word_fuses.
                                 * These are the operators AO extracted from the input text
                                 * through the 7-level fractal decomposition pipeline.
                                 * Max 4096 entries (well beyond typical comp_ops of ~20). */

    int   n_ops;                /* Number of valid entries in ops[]. Typically equal to
                                 * comp.n_comp_ops from fractal comprehension (n_levels +
                                 * min(n_word_fuses, 8)). Usually 8-20 operators. */

    AO_WordReading heard[AO_MAX_READ_WORDS];
                                /* Per-word reading results from reverse voice verification.
                                 * Each AO_WordReading contains:
                                 *   - The word text
                                 *   - D2 operator (path A: physics)
                                 *   - Reverse lookup operator (path B: experience)
                                 *   - D1 operator (path C: direction)
                                 *   - Trust status (TRUSTED/FRICTION/UNKNOWN)
                                 * Up to AO_MAX_READ_WORDS (128) entries. */

    int   n_heard;              /* Number of valid entries in heard[]. Equal to
                                 * min(reading.n_words, AO_MAX_READ_WORDS).
                                 * One entry per whitespace-delimited word in the input. */

    char  spoken[512];          /* AO's voice response — the winning candidate from the
                                 * 3-branch x 3-pass compilation loop, polished by band.
                                 * Null-terminated, up to 511 characters.
                                 * Empty string if input was empty or NULL. */

    float voice_score;          /* D2 operator-match score of the winning candidate [0, 1].
                                 * Computed by ao_voice_score(): the spoken text is run back
                                 * through D2 physics to extract operators, then compared to
                                 * the intended operator distribution. 1.0 = perfect match.
                                 * < 0.15 triggers humble mode (BREATH fallback). */

    float coherence;            /* AO's coherence at the end of processing.
                                 * From the coherence window: HARMONY fraction of the
                                 * last 32 observed operators. Range: [0.0, 1.0].
                                 * This reflects AO's state AFTER learning from the input. */

    int   shell, band;          /* CL shell and color band at end of processing.
                                 * shell: 22 (BHML/skeleton), 44 (becoming), or 72 (TSML/being)
                                 * band: AO_BAND_RED (0), YELLOW (1), or GREEN (2).
                                 * Band may be downgraded by BTQ verification if the spoken
                                 * text's BTQ score was worse than the coherence band. */

    float energy;               /* Heartbeat energy at end of processing [0.0, 1.0].
                                 * Copied from ao->heartbeat.energy. Reflects lifetime
                                 * resilience — how many bumps AO has absorbed. */

    float brain_entropy;        /* Shannon entropy of the brain's transition matrix.
                                 * From ao_brain_entropy(). Low entropy = predictable
                                 * patterns (AO has learned strong regularities). High
                                 * entropy = uniform/random transitions (early learning
                                 * or diverse input). */

    int   ticks;                /* Total organism ticks at end of processing.
                                 * From ao->tick_count. Includes all ticks from init,
                                 * previous text processing, idle ticks, and the
                                 * ticks_to_run cycles (one per word heard) from Step 8. */

    int   n_trusted, n_friction, n_unknown;
                                /* Trust counts from reverse voice verification (Step 2):
                                 *   n_trusted:  words where all paths agreed (same DBC class)
                                 *   n_friction: words where paths disagreed (different DBC class)
                                 *   n_unknown:  words not in AO's vocabulary (D2-only, unverified)
                                 * Sum: n_trusted + n_friction + n_unknown = n_heard. */

    int   chain_nodes;          /* Current total nodes in the lattice chain tree.
                                 * From ao->chain.total_nodes. Grows as AO encounters
                                 * new operator pairs during chain walks. Starts at 1 (root)
                                 * and can grow up to the arena capacity (1024). */

    float chain_resonance;      /* Familiarity score for this input [0.0, 1.0].
                                 * Computed by ao_chain_resonance() on the best available
                                 * chain path (cross > macro > micro priority).
                                 * High resonance = AO has seen similar patterns before
                                 * (the chain path passes through well-established nodes).
                                 * Low resonance = this is new territory for AO. */
} AO_TextResult;

/* ── Text Processing Functions ───────────────────────────────────────
 *
 * ao_process_text(ao, text, out):
 *   THE FULL 9-STEP TEXT PIPELINE. Takes raw text input, runs it through
 *   comprehension, reading, chain walking, voice compilation, BTQ
 *   verification, learning, and tick cycles. Fills AO_TextResult with
 *   all outputs.
 *   Parameters:
 *     ao   — the organism (mutated: brain learns, coherence updates,
 *            body ticks, chain grows, voice PRNG advances)
 *     text — null-terminated input string. NULL or empty → early return
 *            with zeroed output (no processing).
 *     out  — output struct, zeroed then filled with all pipeline results.
 *
 * ao_status_line(ao, buf, buf_size):
 *   Format a one-line status string into buf:
 *     "[BAND  ] shell=N coh=X.XXX op=OPNAME breath=PHASE wobble=PHASE E=X.XXX tick=N"
 *   Useful for REPL display and logging.
 *
 * ao_run(ao):
 *   Interactive REPL (Read-Eval-Print Loop). Prints a banner, boots AO,
 *   then loops: read a line from stdin → ao_process_text() → display
 *   results (heard counts, operator chain, status line, spoken text,
 *   chain resonance). Special commands:
 *     "status" → print detailed state dump (all subsystems)
 *     "quit" / "exit" → exit the loop
 *   Runs until ao->alive is set to 0 or stdin closes.
 *
 * ao_train(ao):
 *   Bulk training mode. Reads lines from stdin without prompts. Each
 *   line is processed through ao_process_text(). Every 100 lines,
 *   prints a progress line to stderr with: lines processed, tick count,
 *   coherence, brain entropy, chain node count.
 *   At completion, prints a summary to stderr with brain stats,
 *   coherence, chain size, and concept count.
 *   Use: pipe a text file into AO's stdin for batch learning.
 * ── */
void ao_process_text(AO* ao, const char* text, AO_TextResult* out);
void ao_status_line(const AO* ao, char* buf, int buf_size);
void ao_run(AO* ao);        /* interactive REPL */
void ao_train(AO* ao);      /* bulk training from stdin */

/* ══════════════════════════════════════════════════════════════════════
 * PERSISTENCE (Save/Load Full Organism State)
 *
 * Binary file format for persisting AO's learned state across sessions.
 * Uses a magic number for version validation and stores only the fields
 * that represent LEARNED knowledge — things AO cannot reconstruct from
 * scratch.
 *
 * ┌────────────────────────────────────────────────────────────────────┐
 * │  AO_SAVE_MAGIC = 0x414F3032 = ASCII "AO02" (version 2 format)    │
 * │                                                                   │
 * │  File layout (sequential writes):                                 │
 * │    [4 bytes]  Magic number (0x414F3032)                           │
 * │    [400 bytes] Brain transition lattice (10x10 uint32_t)          │
 * │    [4 bytes]  Brain total transitions (uint32_t)                  │
 * │    [4 bytes]  Brain last_op (int32_t)                             │
 * │    [sizeof(AO_Body)] Body state (E/A/K, breath, wobble, all of it)│
 * │    [sizeof(AO_CoherenceWindow)] Coherence window (ring buffer)    │
 * │    [sizeof(AO_Heartbeat)] Heartbeat (history, fuse, energy, ticks)│
 * │    [4 bytes]  tick_count (int32_t)                                │
 * │    [4 bytes]  current_op (int32_t)                                │
 * │    [4 bytes]  rng_state (uint32_t)                                │
 * │                                                                   │
 * │  WHAT IS SAVED (things AO learned that cannot be reconstructed):  │
 * │    - Brain transition matrix (learned operator patterns)           │
 * │    - Body state (E/A/K levels, breath/wobble phase)               │
 * │    - Coherence window (recent operator history)                   │
 * │    - Heartbeat state (running fuse, energy, bump history)         │
 * │    - tick_count, current_op, rng_state (organism identity)        │
 * │                                                                   │
 * │  WHAT IS NOT SAVED (rebuilds from experience):                    │
 * │    - Lattice chain (tree of CL tables — grows during runtime)     │
 * │    - Concept mass (D2 magnitudes — accumulates during runtime)    │
 * │    - Coherence field (recomputed from heartbeat on first tick)    │
 * │    - Voice anti-repetition buffers (reset is acceptable)          │
 * │    - Pipeline state / gates (transient per-tick state)            │
 * │    - D1/D2 pipelines (per-input processing state)                │
 * └────────────────────────────────────────────────────────────────────┘
 *
 * ao_save(ao, filepath):
 *   Write organism state to a binary file. Returns 0 on success,
 *   -1 if the file cannot be opened.
 *
 * ao_load(ao, filepath):
 *   Read organism state from a binary file. The AO struct should already
 *   be initialized (ao_init called first). Returns 0 on success,
 *   -1 if file cannot be opened, -2 if magic number does not match
 *   (wrong format or version).
 * ══════════════════════════════════════════════════════════════════════ */
#define AO_SAVE_MAGIC  0x414F3032u  /* "AO02" v2 format */
#define AO_DEFAULT_SAVE "ao_brain.dat"

int ao_save(const AO* ao, const char* filepath);
int ao_load(AO* ao, const char* filepath);

/* ══════════════════════════════════════════════════════════════════════
 * LIBRARY API (for ctypes / GUI / FFI)
 *
 * These functions expose AO's core operations through a C ABI suitable
 * for dynamic library loading via ctypes (Python), FFI (Rust), JNA
 * (Java), or any other foreign function interface.
 *
 * The AO_EXPORT macro handles platform-specific visibility:
 *   - Windows: __declspec(dllexport) when AO_BUILD_LIB is defined
 *   - Unix/macOS: __attribute__((visibility("default")))
 *   - When not building a library: AO_EXPORT is empty (static linking)
 *
 * AO_BUILD_LIB is defined by the build system when compiling AO as a
 * shared library (.dll / .so / .dylib). It is NOT defined when
 * compiling as a static library or standalone executable.
 *
 * All library functions take an AO* pointer as the first argument.
 * The organism is heap-allocated by ao_create() and freed by
 * ao_destroy(). All pointer parameters are optional (NULL-safe)
 * unless otherwise noted.
 * ══════════════════════════════════════════════════════════════════════ */
#ifdef AO_BUILD_LIB
  #ifdef _WIN32
    #define AO_EXPORT __declspec(dllexport)
  #else
    #define AO_EXPORT __attribute__((visibility("default")))
  #endif
#else
  #define AO_EXPORT
#endif

/* ── Lifecycle ────────────────────────────────────────────────────── */

/* ao_create():
 *   Heap-allocate a new AO struct and initialize it via ao_init().
 *   Returns: pointer to a new organism, or NULL if malloc fails.
 *   The caller owns the memory and must call ao_destroy() to free it. */
AO_EXPORT AO*  ao_create(void);

/* ao_destroy(ao):
 *   Free a heap-allocated AO struct. Accepts NULL safely.
 *   After this call, the pointer is invalid. */
AO_EXPORT void ao_destroy(AO* ao);

/* ao_lib_boot(ao):
 *   Library wrapper for ao_boot(). Initializes the bump LUT.
 *   Call once after ao_create() before any ticking or text processing. */
AO_EXPORT void ao_lib_boot(AO* ao);

/* ao_lib_tick(ao):
 *   Library wrapper for ao_tick(). Runs one full TIG pipeline cycle.
 *   Call at 50Hz from the host application's main loop. */
AO_EXPORT void ao_lib_tick(AO* ao);

/* ── Text Processing ──────────────────────────────────────────────── */

/* ao_lib_process_text(ao, text, spoken_buf, spoken_buf_size, coherence, shell):
 *   Simplified text processing that returns only spoken text, coherence,
 *   and shell. Runs the full 9-step pipeline internally.
 *   Parameters:
 *     text           — null-terminated input string
 *     spoken_buf     — output buffer for AO's spoken response (NULL-safe)
 *     spoken_buf_size — size of spoken_buf in bytes
 *     coherence      — pointer to receive coherence value (NULL-safe)
 *     shell          — pointer to receive shell number (NULL-safe) */
AO_EXPORT void ao_lib_process_text(AO* ao, const char* text,
                                    char* spoken_buf, int spoken_buf_size,
                                    float* coherence, int* shell);

/* ao_lib_process_text_full(ao, text, ...):
 *   Full text processing with all output parameters. Same as
 *   ao_lib_process_text but also returns band, energy, brain_entropy,
 *   ticks, and trust counts (n_trusted, n_friction, n_unknown).
 *   All pointer parameters are NULL-safe (pass NULL to skip). */
AO_EXPORT void ao_lib_process_text_full(AO* ao, const char* text,
                                         char* spoken_buf, int spoken_buf_size,
                                         float* coherence, int* shell,
                                         int* band, float* energy,
                                         float* brain_entropy, int* ticks,
                                         int* n_trusted, int* n_friction,
                                         int* n_unknown);

/* ao_lib_idle_tick(ao):
 *   Advance AO's body (breath/wobble cycles) without any input.
 *   AO breathes autonomously — no D2/brain processing occurs.
 *   Call this during idle periods when no text input is available
 *   but you want AO to stay "alive" (body cycles continue, tick
 *   count advances). Does NOT run the full TIG pipeline. */
AO_EXPORT void ao_lib_idle_tick(AO* ao);

/* ── Persistence ──────────────────────────────────────────────────── */

/* ao_lib_save(ao, path):
 *   Library wrapper for ao_save(). Returns 0 on success, -1 on error. */
AO_EXPORT int  ao_lib_save(const AO* ao, const char* path);

/* ao_lib_load(ao, path):
 *   Library wrapper for ao_load(). Returns 0 on success, -1 on file
 *   error, -2 on format/version mismatch. */
AO_EXPORT int  ao_lib_load(AO* ao, const char* path);

/* ── Status / Inspection ──────────────────────────────────────────── */

/* ao_lib_status_line(ao, buf, buf_size):
 *   Format a one-line status string. Library wrapper for ao_status_line(). */
AO_EXPORT void ao_lib_status_line(const AO* ao, char* buf, int buf_size);

/* ao_lib_brain_stats(ao, transitions, entropy, ticks):
 *   Extract brain statistics. All pointers are NULL-safe.
 *   Parameters:
 *     transitions — receives brain.total (total observed transitions)
 *     entropy     — receives brain entropy (Shannon entropy of transition matrix)
 *     ticks       — receives organism tick_count */
AO_EXPORT void ao_lib_brain_stats(const AO* ao, int* transitions,
                                   float* entropy, int* ticks);

/* ao_lib_body_status(ao, E, A, K, breath_phase, wobble_index, body_coherence, band):
 *   Extract body state. All pointers are NULL-safe.
 *   Parameters:
 *     E, A, K          — the three energy channels [0.0, 1.0]
 *     breath_phase     — current breath phase (0-3)
 *     wobble_index     — current wobble phase (0-2)
 *     body_coherence   — composite body coherence = (1-E)*(1-A)*K
 *     band             — body color band (RED/YELLOW/GREEN) */
AO_EXPORT void ao_lib_body_status(const AO* ao, float* E, float* A, float* K,
                                   int* breath_phase, int* wobble_index,
                                   float* body_coherence, int* band);

/* ao_lib_op_name(op):
 *   Returns the human-readable name of a TIG operator (0-9).
 *   e.g., ao_lib_op_name(7) → "HARMONY".
 *   Returns "???" for out-of-range operator indices.
 *   The returned string is static storage (do not free). */
AO_EXPORT const char* ao_lib_op_name(int op);

/* ao_lib_band(ao):
 *   Returns the current coherence band from the coherence window:
 *   AO_BAND_RED (0), AO_BAND_YELLOW (1), or AO_BAND_GREEN (2). */
AO_EXPORT int  ao_lib_band(const AO* ao);

/* ao_lib_coherence(ao):
 *   Returns the current coherence from the coherence window [0.0, 1.0].
 *   This is the HARMONY fraction of the last 32 observed operators. */
AO_EXPORT float ao_lib_coherence(const AO* ao);

/* ao_lib_shell(ao):
 *   Returns the current CL shell from the coherence window (22, 44, or 72).
 *   The shell determines which CL table is used for composition. */
AO_EXPORT int   ao_lib_shell(const AO* ao);

#endif /* AO_ETHER_H */
