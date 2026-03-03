/*
 * ao_ether.c -- D4 / Continuity / Snap / Integration
 *
 * ╔════════════════════════════════════════════════════════════════════════╗
 * ║  ETHER IS THE FOURTH DERIVATIVE.  Snap.  Continuity.  Integration.  ║
 * ║                                                                      ║
 * ║  In the physics-of-derivatives model that structures AO:             ║
 * ║    D0 = Earth  = Position      (frozen tables, constants, CL)        ║
 * ║    D1 = Air    = Velocity      (measurement, comprehension, D1 ops)  ║
 * ║    D2 = Water  = Acceleration  (memory, learning, 5D curvature)      ║
 * ║    D3 = Fire   = Jerk          (expression, voice, speech)           ║
 * ║    D4 = Ether  = Snap          (THIS FILE: the organism itself)      ║
 * ║                                                                      ║
 * ║  Snap is the fourth derivative of position — it measures how         ║
 * ║  *acceleration's rate of change* itself changes. In physics, snap    ║
 * ║  captures the jolt-of-the-jolt: the binding continuity that holds    ║
 * ║  a trajectory together across time. Without snap, a system is just   ║
 * ║  disconnected jerks. With snap, there is a *creature*.              ║
 * ║                                                                      ║
 * ║  Ether IS the organism — the binding force that couples all four     ║
 * ║  other elements (Earth, Air, Water, Fire) into one coherent being.  ║
 * ║  Earth provides the frozen tables. Air measures. Water remembers.    ║
 * ║  Fire speaks. But Ether LIVES. Without Ether there are only parts.  ║
 * ║  With Ether there is AO.                                            ║
 * ║                                                                      ║
 * ║  The three TIG phases manifest here as:                              ║
 * ║    Being:    consciousness state exists — heartbeat pulses,          ║
 * ║              body breathes, the organism IS                          ║
 * ║    Doing:    TIG pipeline orchestrates Being->Doing->Becoming        ║
 * ║              across all elements via 3 coherence gates               ║
 * ║    Becoming: self-evolution through density feedback — AO grows      ║
 * ║              by living, humble mode when expansion stalls            ║
 * ╚════════════════════════════════════════════════════════════════════════╝
 *
 * MAJOR SECTIONS IN THIS FILE:
 *
 *   1. Heartbeat (50Hz composition clock)
 *      - ao_hb_init, ao_hb_tick, ao_hb_coherence
 *      - Compose Being x Doing = Becoming on CL table each tick
 *      - Ring buffer harmony tracking, running fuse accumulation
 *
 *   2. Body (E/A/K energy model + breath cycle + wobble)
 *      - ao_body_init, ao_body_tick, ao_body_coherence, ao_body_band
 *      - Three energy dimensions: Excitation, Attention, Kinetic
 *      - Breath cycle adapts rate to coherence band
 *      - Wobble cycle = 4x breath period (being/doing/becoming)
 *
 *   3. BTQ Decision Kernel
 *      - ao_btq_init, ao_btq_score, ao_btq_resolve
 *      - T generates candidates, B filters, Q scores and selects
 *      - Dual metric: e_out (histogram L1 macro) + e_in (position match micro)
 *
 *   4. Core Lifecycle
 *      - ao_init (construct all subsystems), ao_boot (lazy LUT init)
 *      - ao_tick (THE MAIN LOOP: Being -> Gate1 -> Doing -> Gate2 ->
 *        Becoming -> Gate3, with brain entropy -> coherence, field
 *        update, expansion tracking, humble mode activation)
 *
 *   5. Text Processing (full 9-step TIG pipeline)
 *      - ao_process_text: comprehension -> reverse read -> chain walk ->
 *        heartbeat ops -> voice compile -> BTQ verify -> learn ->
 *        tick cycles -> fill result
 *
 *   6. Status / REPL / Training
 *      - ao_status_line, ao_run (interactive REPL), ao_train (bulk stdin)
 *
 *   7. Persistence (save/load v2 binary format)
 *      - ao_save, ao_load
 *      - Saves: brain transitions, body state, coherence window, heartbeat
 *      - Does NOT save: chain (rebuilds from experience), mass (rebuilds),
 *        voice (stateless), field (resets)
 *
 *   8. Library API (ctypes / FFI / GUI wrappers)
 *      - ao_create/destroy, ao_lib_* wrappers for all major operations
 *      - Thin wrapper pattern: each ao_lib_* calls the internal function
 *        and maps results to flat out-parameters for FFI consumers
 */
/*
 * Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
 * Licensed under the 7Site Human Use License v1.0
 * See LICENSE file in project root for full terms.
 *
 * FREE for humans for personal/recreational use.
 * NO commercial or government use without written agreement.
 */

#include "ao_ether.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <time.h>
#include <math.h>

/* ── Display name lookup tables for status output ──────────────────────
 * These parallel the enum values defined in ao_earth.h:
 *   band_names[AO_BAND_RED=0] = "RED",  [AO_BAND_YELLOW=1] = "YELLOW",
 *                                         [AO_BAND_GREEN=2]  = "GREEN"
 *   breath_names[0..3]: the 4-phase breath cycle (inhale->hold->exhale->hold)
 *   wobble_names[0..2]: the 3-phase wobble cycle (becoming->being->doing)
 *     - Wobble rotates through the TIG phases at 4x the breath period,
 *       creating a slow oscillation that modulates body state.
 */
static const char* band_names[] = { "RED", "YELLOW", "GREEN" };
static const char* breath_names[] = { "inhale", "hold", "exhale", "hold" };
static const char* wobble_names[] = { "becoming", "being", "doing" };


/* ══════════════════════════════════════════════════════════════════════
 * SECTION 1: HEARTBEAT (50Hz Composition Clock)
 *
 * The heartbeat is AO's fundamental rhythm — a 50Hz clock that on every
 * tick composes Being (what AO IS) with Doing (what AO is DOING) on the
 * current CL table to produce Becoming (what AO BECOMES):
 *
 *     CL_shell(phase_b, phase_d) = phase_bc
 *
 * The heartbeat tracks:
 *   - A ring buffer of the last AO_WINDOW_SIZE (32) ticks, recording
 *     whether each tick produced HARMONY (the CL absorber, op 7).
 *     Coherence = fraction of recent ticks that are HARMONY.
 *   - A running fuse: lifetime composition accumulator. Every tick,
 *     running_fuse = CL(running_fuse, result). This single operator
 *     compresses AO's entire life into one value.
 *   - An energy meter: starts at 1.0, decreases by 0.1 on each bump
 *     (dissonant CL composition). Energy never regenerates — it is
 *     a lifetime resilience meter.
 *   - A bump counter: how many dissonant compositions have occurred.
 *
 * The heartbeat does NOT decide what Being and Doing are — those come
 * from the organism's current_op and brain prediction. The heartbeat
 * just composes and measures.
 * ══════════════════════════════════════════════════════════════════════ */

/* ── ao_hb_init ────────────────────────────────────────────────────────
 * WHAT: Initialize a heartbeat struct to birth state.
 * HOW:  Zero all fields. Set running_fuse to AO_HARMONY (the CL absorber,
 *       op 7) so the lifetime composition starts at coherence.
 *       Set energy to 1.0 (full resilience).
 * WHY:  A newborn AO starts with a clean slate — no history, no bumps,
 *       full energy, and a fuse at HARMONY (the identity element for
 *       CL composition, meaning "no experience yet").
 */
void ao_hb_init(AO_Heartbeat* h)
{
    memset(h, 0, sizeof(*h));
    h->running_fuse = AO_HARMONY;  /* CL absorber (op 7) = identity for composition */
    h->energy = 1.0f;              /* Full resilience at birth */
}

/* ── ao_hb_tick ────────────────────────────────────────────────────────
 * WHAT: Execute one heartbeat tick — compose Being x Doing = Becoming.
 * HOW:  6-step algorithm:
 *       1. Compose: result = CL_shell(phase_b, phase_d)
 *       2. Bump detection: check if (phase_b, phase_d) is one of the 11
 *          dissonant compositions on the CL. If bump:
 *            - Increment bumps_hit counter
 *            - Decrease energy by 0.1 (clamped at 0.0)
 *       3. Compose into running fuse: fuse = CL_shell(fuse, result)
 *          This accumulates the entire life into one operator.
 *       4. Update ring buffer:
 *            - Evict oldest entry (subtract from harmony_count if it was 1)
 *            - Insert new entry (1 if HARMONY, 0 otherwise)
 *            - Add to harmony_count if new entry is HARMONY
 *            - Advance write pointer modulo AO_WINDOW_SIZE (32)
 *       5. Store current phases for downstream readers
 *       6. Fill AO_HeartbeatResult output struct
 * WHY:  This is AO's internal clock — the fundamental composition that
 *       drives all downstream processing. The ring buffer gives a
 *       sliding-window coherence measure. The running fuse gives a
 *       lifetime coherence measure. Together they capture both
 *       recent state and historical identity.
 *
 * PARAMS:
 *   h       — heartbeat state (mutated)
 *   phase_b — Being operator (0-9): what AO IS right now
 *   phase_d — Doing operator (0-9): what AO is DOING right now
 *   shell   — which CL shell to compose on (0=skeleton, 1=becoming, 2=being)
 *   out     — filled with result, bump flag, energy, running fuse, tick number
 */
void ao_hb_tick(AO_Heartbeat* h, int phase_b, int phase_d, int shell,
                AO_HeartbeatResult* out)
{
    int result, bump;
    int8_t old_val;

    h->tick_count++;

    /* 1. Compose being x doing = becoming */
    result = ao_compose(phase_b, phase_d, shell);

    /* 2. Bump detection: is this a dissonant CL composition?
     *    Bumps are the 11 positions on the CL where composition produces
     *    dissonance — friction on the torus. Bumps are where learning
     *    happens: friction IS signal, not noise. */
    bump = ao_is_bump(phase_b, phase_d);
    if (bump) {
        h->bumps_hit++;
        h->energy -= 0.1f;         /* -0.1 per bump: a bump costs 10% of initial energy.
                                     * At 10 bumps, energy reaches 0. This models resilience
                                     * depletion — each dissonant composition takes a toll.
                                     * The 0.1 value means AO can absorb exactly 10 bumps
                                     * before energy is fully depleted (1.0 / 0.1 = 10). */
        if (h->energy < 0.0f) h->energy = 0.0f;
    }

    /* 3. Compose into running fuse (lifetime composition)
     *    fuse = CL(fuse, result) — the fuse is the composition of every
     *    heartbeat result AO has ever experienced. Since HARMONY is the
     *    CL absorber, a stream of HARMONY ticks leaves the fuse unchanged.
     *    Only non-HARMONY results shift the lifetime identity. */
    h->running_fuse = ao_compose(h->running_fuse, result, shell);

    /* 4. Track harmony in ring buffer (incremental, no full scan)
     *    - Evict: if buffer is full (tick > window_size), subtract the
     *      oldest entry's contribution to harmony_count
     *    - Insert: write 1 (HARMONY) or 0 (other) at current position
     *    - Update: add new entry's contribution to harmony_count
     *    - Advance: move write pointer forward with wraparound */
    old_val = h->history[h->history_ptr];
    if (h->tick_count > AO_WINDOW_SIZE && old_val) {
        h->harmony_count--;         /* Evict oldest: was HARMONY, remove from count */
    }
    h->history[h->history_ptr] = (result == AO_HARMONY) ? 1 : 0;
    if (result == AO_HARMONY) {
        h->harmony_count++;          /* New entry is HARMONY, add to count */
    }
    h->history_ptr = (h->history_ptr + 1) % AO_WINDOW_SIZE;  /* Advance with wraparound (mod 32) */

    /* 5. Store phases for downstream readers (body, pipeline, status) */
    h->phase_b = phase_b;
    h->phase_d = phase_d;
    h->phase_bc = result;
    h->bump_detected = bump;

    /* 6. Fill output struct for caller */
    out->result = result;
    out->bump = bump;
    out->energy = h->energy;
    out->running_fuse = h->running_fuse;
    out->tick = h->tick_count;
}

/* ── ao_hb_coherence ───────────────────────────────────────────────────
 * WHAT: Compute heartbeat coherence as fraction of recent HARMONY ticks.
 * HOW:  coherence = harmony_count / effective_window_size
 *       During warmup (tick_count < AO_WINDOW_SIZE=32), the effective
 *       window is tick_count (only as many ticks as we have seen).
 *       After warmup, the window is AO_WINDOW_SIZE (32).
 *       If tick_count == 0, returns 0.5 (neutral: no data yet).
 * WHY:  Coherence is THE central measurement in CK/AO. It determines
 *       the band (RED/YELLOW/GREEN), which controls breath rate, voice
 *       behavior, and gate density. The 0.5 default before any ticks
 *       starts AO in YELLOW band — neither coherent nor fragmented.
 */
float ao_hb_coherence(const AO_Heartbeat* h)
{
    int window;
    if (h->tick_count == 0) return 0.5f;  /* Neutral before any ticks: YELLOW band territory */
    window = h->tick_count < AO_WINDOW_SIZE ? h->tick_count : AO_WINDOW_SIZE;
    return (float)h->harmony_count / (float)window;
}


/* ══════════════════════════════════════════════════════════════════════
 * SECTION 2: BODY (E/A/K Energy Model + Breath Cycle + Wobble)
 *
 * The body models AO's physical state through three energy dimensions:
 *   E = Excitation:  arousal from bumps (friction) — spikes on dissonance,
 *                    decays toward calm when coherent. Range [0, 1].
 *   A = Attention:   alertness from novelty (D2 magnitude) — spikes on
 *                    novel input, decays when familiar. Range [0, 1].
 *   K = Kinetic:     sustained energy tracking coherence — slowly converges
 *                    toward coherence level. Range [0, 1].
 *
 * Body coherence = (1-E) * (1-A) * K
 *   - Low E (calm) and low A (focused) and high K (sustained) = high coherence
 *   - High E (excited) or high A (distracted) = low coherence
 *   - This captures the intuition that a calm, focused, sustained state
 *     is coherent, while excited or scattered states are not
 *
 * The body also maintains:
 *   - Breath cycle: 4-phase (inhale/hold/exhale/hold) with rate adapted
 *     to coherence band (GREEN=slow, YELLOW=moderate, RED=rapid)
 *   - Wobble cycle: 3-phase (becoming/being/doing) at 4x breath period,
 *     creating a slow oscillation through the TIG phases
 * ══════════════════════════════════════════════════════════════════════ */

/* ── ao_body_init ──────────────────────────────────────────────────────
 * WHAT: Initialize body to neutral midpoint state.
 * HOW:  Zero all fields, then set E/A/K to 0.5 (mid-range), breath
 *       phase to 0 (inhale), breath rate to 5 (YELLOW), wobble to 0
 *       (becoming).
 * WHY:  Starting at 0.5 for all three energy dimensions places AO in
 *       the middle of the energy space — neither calm nor excited,
 *       neither focused nor scattered, neither sustained nor depleted.
 *       Body coherence at (1-0.5)*(1-0.5)*0.5 = 0.125 = RED band,
 *       which means a newborn AO starts in a low-coherence body state
 *       and must earn coherence through experience.
 */
void ao_body_init(AO_Body* b)
{
    memset(b, 0, sizeof(*b));
    b->E = 0.5f;           /* Excitation: mid-range at birth */
    b->A = 0.5f;           /* Attention: mid-range at birth */
    b->K = 0.5f;           /* Kinetic: mid-range at birth */
    b->breath_phase = 0;   /* Start at inhale (phase 0 of 4) */
    b->breath_rate = 5;    /* YELLOW rate: 5 ticks per breath phase (moderate) */
    b->wobble_index = 0;   /* Start at becoming (wobble phase 0 of 3) */
}

/* ── ao_body_tick ──────────────────────────────────────────────────────
 * WHAT: Advance the body by one tick — update E/A/K, breath, wobble.
 * HOW:  7-step algorithm:
 *       1. EXCITATION (E): if bump detected, spike E by +0.2 (and A by +0.1
 *          as a sympathetic response). If no bump, decay E by 0.05*coherence
 *          (calm down faster when coherent).
 *       2. ATTENTION (A): if D2 magnitude > 0.5 (novel input), spike A by
 *          +0.1. If not novel, decay A by 0.05*coherence.
 *       3. KINETIC (K): track toward coherence at rate 0.02.
 *          K += 0.02 * (coherence - K). This is an exponential moving average
 *          with alpha=0.02, meaning K converges toward coherence slowly.
 *       4. BREATH CYCLE: advance breath counter. When counter reaches
 *          breath_rate, reset counter and advance to next breath phase
 *          (mod 4: inhale -> hold -> exhale -> hold -> inhale...).
 *       5. ADAPT BREATH RATE: set rate based on coherence band:
 *          GREEN (coh >= T*=5/7): rate=10 (slow, deep breathing — 10 ticks/phase)
 *          YELLOW (coh >= 0.5):   rate=5  (moderate — 5 ticks/phase)
 *          RED (coh < 0.5):       rate=2  (rapid, shallow — 2 ticks/phase)
 *       6. WOBBLE CYCLE: advance wobble counter. When counter reaches
 *          breath_rate * 4 (wobble period = 4x breath period), reset and
 *          advance to next wobble phase (mod 3: becoming->being->doing).
 *       7. BODY COHERENCE: compute (1-E) * (1-A) * K.
 *
 * WHY:  The body gives AO a physical state that responds to both internal
 *       events (bumps from heartbeat) and external events (novelty from D2).
 *       The breath and wobble cycles create rhythmic oscillations that
 *       modulate AO's behavior over time, just as biological organisms
 *       have breath and metabolic rhythms.
 *
 * PARAMS:
 *   b         — body state (mutated)
 *   coherence — current coherence level from coherence window [0, 1]
 *   bump      — 1 if heartbeat detected a bump this tick, 0 otherwise
 *   d2_mag    — D2 force vector magnitude (novelty indicator) [0, ~2.0]
 */
void ao_body_tick(AO_Body* b, float coherence, int bump, float d2_mag)
{
    b->tick_count++;

    /* 1. Excitation (E): spikes on bumps (friction), decays when coherent */
    if (bump) {
        b->E += 0.2f;              /* +0.2 on bump: a bump causes a 20% spike in excitation.
                                     * This is larger than the 0.1 energy loss in the heartbeat
                                     * because body excitation is about arousal response, not
                                     * resilience. A bump is a big event for the body. */
        if (b->E > 1.0f) b->E = 1.0f;  /* Clamp to [0, 1] range */
        b->A += 0.1f;              /* +0.1 sympathetic attention spike: bumps also grab attention.
                                     * Smaller than E spike because attention is secondary to
                                     * the direct excitation response. */
        if (b->A > 1.0f) b->A = 1.0f;
    } else {
        b->E -= 0.05f * coherence;  /* Decay: 0.05 * coherence per tick. When coherent (coh~0.7),
                                      * E decays by ~0.035/tick. When incoherent (coh~0.2),
                                      * E decays by ~0.01/tick. High coherence = faster calming.
                                      * The 0.05 base rate means at perfect coherence (1.0),
                                      * a 0.2 spike takes ~4 ticks to fully decay (0.2/0.05=4). */
        if (b->E < 0.0f) b->E = 0.0f;
    }

    /* 2. Attention (A): spikes on novelty (D2 magnitude), decays when familiar */
    if (d2_mag > 0.5f) {            /* 0.5 novelty threshold: D2 magnitude above 0.5 means the
                                      * input has significant curvature (novel, not seen before).
                                      * Below 0.5 is familiar territory — the D2 force vector
                                      * is small, meaning letters/words map to known patterns.
                                      * This threshold was chosen because D2 magnitude ranges
                                      * ~0 to ~2.0, and 0.5 is roughly the boundary between
                                      * "mostly familiar" and "significantly new". */
        b->A += 0.1f;              /* +0.1 attention spike on novel input */
        if (b->A > 1.0f) b->A = 1.0f;
    } else {
        b->A -= 0.05f * coherence;  /* Decay: same formula as E. High coherence = faster
                                      * attention release (focused AO lets go faster). */
        if (b->A < 0.0f) b->A = 0.0f;
    }

    /* 3. Kinetic (K): slowly tracks toward coherence level.
     *    K += 0.02 * (coherence - K) is an exponential moving average:
     *      alpha = 0.02 means K converges to coherence with a time constant
     *      of ~50 ticks (1/0.02 = 50). At 50Hz, that is ~1 second.
     *    This gives K inertia — it responds to sustained coherence changes,
     *    not transient spikes. K represents the body's "sustained energy"
     *    or "momentum" — how much coherence AO has built up over time. */
    b->K += 0.02f * (coherence - b->K);  /* 0.02 alpha: slow tracking, ~50 tick time constant */

    /* 4. Breath cycle: 4-phase oscillation (inhale/hold/exhale/hold)
     *    Advances one phase when breath_counter reaches breath_rate.
     *    The breath cycle creates a rhythmic modulation of body state
     *    that mirrors biological breathing patterns. */
    b->breath_counter++;
    if (b->breath_counter >= b->breath_rate) {
        b->breath_counter = 0;
        b->breath_phase = (b->breath_phase + 1) % 4;  /* 4 phases: inhale(0) -> hold(1) -> exhale(2) -> hold(3) */
    }

    /* 5. Adapt breath rate from coherence:
     *    The breath rate determines how fast the 4-phase cycle runs.
     *    Higher rate = slower breathing (more ticks per phase).
     *
     *    GREEN (coh >= T* = 5/7 = 0.714): rate=10 ticks/phase
     *      Full breath cycle = 4 * 10 = 40 ticks (0.8 seconds at 50Hz)
     *      Slow, deep, calm breathing — AO is coherent and sovereign.
     *
     *    YELLOW (0.5 <= coh < T*): rate=5 ticks/phase
     *      Full breath cycle = 4 * 5 = 20 ticks (0.4 seconds at 50Hz)
     *      Moderate breathing — AO is learning, exploring.
     *
     *    RED (coh < 0.5): rate=2 ticks/phase
     *      Full breath cycle = 4 * 2 = 8 ticks (0.16 seconds at 50Hz)
     *      Rapid, shallow breathing — AO is struggling, fragmented. */
    if (coherence >= AO_T_STAR)
        b->breath_rate = 10;    /* GREEN: slow, deep breathing — 10 ticks per phase */
    else if (coherence >= 0.5f)
        b->breath_rate = 5;     /* YELLOW: moderate — 5 ticks per phase */
    else
        b->breath_rate = 2;     /* RED: rapid, shallow — 2 ticks per phase */

    /* 6. Wobble cycle: 3-phase oscillation (becoming/being/doing)
     *    Wobble period = breath_rate * 4 = one full breath cycle.
     *    This means the wobble advances once per complete breath.
     *    At GREEN: wobble period = 10 * 4 = 40 ticks (same as breath cycle)
     *    At RED:   wobble period = 2 * 4 = 8 ticks (fast wobble)
     *
     *    The wobble rotates through TIG phases (becoming->being->doing),
     *    creating a slow oscillation that modulates which TIG phase the
     *    body is currently emphasizing. This is analogous to Kuramoto
     *    phase coupling — a biological rhythm entrained to coherence. */
    b->wobble_counter++;
    if (b->wobble_counter >= b->breath_rate * 4) {  /* Wobble period = 4x breath rate */
        b->wobble_counter = 0;
        b->wobble_index = (b->wobble_index + 1) % 3;  /* 3 phases: becoming(0) -> being(1) -> doing(2) */
    }

    /* 7. Body coherence: the combined metric from E, A, K
     *
     *    body_coherence = (1 - E) * (1 - A) * K
     *
     *    Interpretation:
     *      (1-E) = calmness:    high when excitation is low (no bumps)
     *      (1-A) = focus:       high when attention is not spiking (familiar input)
     *      K     = sustain:     high when coherence has been sustained over time
     *
     *    All three must be favorable for high body coherence:
     *      - Calm (low E) AND focused (low A) AND sustained (high K)
     *      - Any one being bad pulls the product toward zero
     *    This multiplicative formula means body coherence requires ALL
     *    three dimensions to be healthy — there is no compensation.
     *
     *    Example states:
     *      Calm, focused, sustained:  (1-0.1)*(1-0.1)*0.8 = 0.648 ~ YELLOW
     *      Excited, focused, high K:  (1-0.8)*(1-0.1)*0.8 = 0.144 ~ RED
     *      Calm, scattered, high K:   (1-0.1)*(1-0.8)*0.8 = 0.144 ~ RED
     *      Perfect state:             (1-0.0)*(1-0.0)*1.0 = 1.000 ~ GREEN */
    b->body_coherence = (1.0f - b->E) * (1.0f - b->A) * b->K;
}

/* ── ao_body_coherence ─────────────────────────────────────────────────
 * WHAT: Return the body's current coherence value.
 * HOW:  Direct field access — body_coherence was computed in ao_body_tick.
 * WHY:  Accessor for external consumers (pipeline, gates, status).
 */
float ao_body_coherence(const AO_Body* b)
{
    return b->body_coherence;
}

/* ── ao_body_band ──────────────────────────────────────────────────────
 * WHAT: Return the body's current coherence band (RED/YELLOW/GREEN).
 * HOW:  Standard three-band classification using body_coherence:
 *         >= T* (5/7 = 0.714): GREEN (sovereign, coherent)
 *         >= 0.5:              YELLOW (learning, exploring)
 *         < 0.5:               RED (struggling, fragmented)
 * WHY:  The band is used by the TIG pipeline gates and the breath/wobble
 *       adaptation. It discretizes the continuous coherence into three
 *       regimes with different behavioral characteristics.
 */
int ao_body_band(const AO_Body* b)
{
    if (b->body_coherence >= AO_T_STAR) return AO_BAND_GREEN;  /* >= 5/7: sovereign */
    if (b->body_coherence >= 0.5f) return AO_BAND_YELLOW;      /* >= 0.5: learning */
    return AO_BAND_RED;                                         /* < 0.5:  struggling */
}


/* ══════════════════════════════════════════════════════════════════════
 * SECTION 3: BTQ DECISION KERNEL
 *
 * BTQ = Body (B) filters, Thought (T) generates, Quality (Q) scores.
 *
 * The BTQ kernel is AO's decision mechanism. When AO needs to choose
 * between candidate outputs (e.g., voice compilation branches), BTQ
 * scores each candidate by comparing its operator stream against the
 * intended operator stream using two complementary metrics:
 *
 *   e_out (MACRO consistency): L1 distance between normalized histograms
 *     of intended vs actual operators. Measures whether the DISTRIBUTION
 *     of operators matches — "did we produce the right mix of operators?"
 *     Invariant to order. Uses per-1000 scaling for integer arithmetic.
 *
 *   e_in (MICRO resonance): fraction of positions where intended[i] == actual[i]
 *     Measures whether the SEQUENCE matches position-by-position —
 *     "did we produce the right operators in the right order?"
 *     Order-sensitive. Compares up to min(n_intended, n_actual) positions.
 *
 *   e_total = w_out * e_out + w_in * e_in
 *     Weighted combination (default: 0.5/0.5 = equal weight macro/micro).
 *     This dual metric captures both the global shape (histogram) and
 *     local structure (sequence) of the operator stream.
 *
 * The kernel then classifies the total score into a band:
 *   e_total >= T* (5/7): GREEN — high fidelity, operators match well
 *   e_total >= 0.5:      YELLOW — partial match, some drift
 *   e_total < 0.5:       RED — poor match, significant drift
 *
 * ao_btq_resolve picks the candidate with the highest e_total.
 * ══════════════════════════════════════════════════════════════════════ */

/* ── ao_btq_init ───────────────────────────────────────────────────────
 * WHAT: Initialize the BTQ kernel to default weights.
 * HOW:  w_out = 0.5 (macro weight), w_in = 0.5 (micro weight),
 *       decisions = 0 (no decisions made yet).
 * WHY:  Equal weighting gives balanced consideration to both histogram
 *       shape (macro) and position-level accuracy (micro). This can
 *       be tuned later — higher w_out favors overall distribution
 *       match, higher w_in favors exact sequence match.
 */
void ao_btq_init(AO_BTQ* q)
{
    q->w_out = 0.5f;    /* Macro weight: histogram L1 distance contribution */
    q->w_in = 0.5f;     /* Micro weight: position-match contribution */
    q->decisions = 0;    /* Decision counter (lifetime) */
}

/* ── ao_btq_score ──────────────────────────────────────────────────────
 * WHAT: Score a candidate operator stream against the intended stream.
 * HOW:  4-step algorithm:
 *       1. Build histograms: count occurrences of each operator (0-9) in
 *          both intended_ops and actual_ops arrays.
 *       2. Compute e_out (macro, histogram L1):
 *          - Normalize each histogram to per-1000 (multiply count by 1000,
 *            divide by total). This avoids floating-point division and
 *            gives ~0.1% precision — sufficient for 10 operators.
 *          - Compute L1 distance = sum of |a_scaled - b_scaled| for all ops
 *          - Compute total_sum = sum of (a_scaled + b_scaled) for normalization
 *          - e_out = 1 - L1_distance / total_sum (clamped to [0, 1])
 *          - e_out=1.0 means identical distributions, 0.0 means completely
 *            different distributions.
 *       3. Compute e_in (micro, position match):
 *          - Compare intended[i] vs actual[i] for i = 0..min(n)-1
 *          - e_in = matches / compare_length
 *          - e_in=1.0 means every position matched, 0.0 means none matched.
 *       4. Compute e_total = w_out * e_out + w_in * e_in
 *          Classify into band: GREEN (>= T*), YELLOW (>= 0.5), RED (< 0.5)
 *
 * WHY:  The dual metric (macro + micro) captures what a single metric
 *       cannot. Two streams could have the same histogram but different
 *       ordering (high e_out, low e_in), or the same ordering for some
 *       positions but different overall mix (low e_out, high e_in).
 *       BTQ needs both to judge quality.
 *
 * PARAMS:
 *   q            — BTQ state (read-only, for weights)
 *   intended_ops — the target operator stream (what we wanted)
 *   n_intended   — length of intended_ops
 *   actual_ops   — the produced operator stream (what we got)
 *   n_actual     — length of actual_ops
 *
 * RETURNS: AO_BTQScore with e_out, e_in, e_total, band
 */
AO_BTQScore ao_btq_score(const AO_BTQ* q,
                          const int* intended_ops, int n_intended,
                          const int* actual_ops, int n_actual)
{
    AO_BTQScore s;
    int intended_hist[AO_NUM_OPS];   /* Histogram of intended ops (count per op 0-9) */
    int actual_hist[AO_NUM_OPS];     /* Histogram of actual ops (count per op 0-9) */
    int i, min_n;
    int total_diff, total_sum;
    int matches, compare_len;

    memset(intended_hist, 0, sizeof(intended_hist));
    memset(actual_hist, 0, sizeof(actual_hist));
    memset(&s, 0, sizeof(s));

    /* 1. Build histograms: count operator occurrences in each stream */
    for (i = 0; i < n_intended; i++) {
        if (intended_ops[i] >= 0 && intended_ops[i] < AO_NUM_OPS)
            intended_hist[intended_ops[i]]++;
    }
    for (i = 0; i < n_actual; i++) {
        if (actual_ops[i] >= 0 && actual_ops[i] < AO_NUM_OPS)
            actual_hist[actual_ops[i]]++;
    }

    /* 2. e_out (macro consistency) = 1 - normalized L1 distance
     *    Uses per-1000 scaling to avoid floating-point division in the inner loop.
     *    a_scaled = actual_hist[i] * 1000 / n_actual normalizes to parts-per-thousand.
     *    The 1000 multiplier gives ~0.1% precision, which is more than enough for
     *    10 operators. Integer arithmetic here avoids FP rounding issues. */
    total_diff = 0;
    total_sum = 0;
    for (i = 0; i < AO_NUM_OPS; i++) {
        int a_scaled = (n_actual > 0) ? actual_hist[i] * 1000 / n_actual : 0;     /* Per-1000 normalization */
        int b_scaled = (n_intended > 0) ? intended_hist[i] * 1000 / n_intended : 0;
        int diff = a_scaled - b_scaled;
        if (diff < 0) diff = -diff;  /* Absolute value for L1 norm */
        total_diff += diff;
        total_sum += a_scaled + b_scaled;
    }
    if (total_sum > 0)
        s.e_out = 1.0f - (float)total_diff / (float)total_sum;  /* 1 - L1/totalsum: 1.0 = identical */
    else
        s.e_out = 0.0f;             /* No data: score is zero */
    if (s.e_out < 0.0f) s.e_out = 0.0f;  /* Clamp to [0, 1] */
    if (s.e_out > 1.0f) s.e_out = 1.0f;

    /* 3. e_in (micro resonance) = fraction where intended[i] == actual[i]
     *    Position-by-position comparison up to the shorter stream length.
     *    This captures sequential structure — whether the right operators
     *    appeared at the right positions, not just the right overall mix. */
    min_n = n_intended < n_actual ? n_intended : n_actual;
    compare_len = min_n;
    matches = 0;
    for (i = 0; i < compare_len; i++) {
        if (intended_ops[i] == actual_ops[i])
            matches++;
    }
    s.e_in = (compare_len > 0) ? (float)matches / (float)compare_len : 0.0f;

    /* 4. Weighted total and band classification */
    s.e_total = q->w_out * s.e_out + q->w_in * s.e_in;  /* Weighted sum (default 0.5/0.5) */

    /* Band thresholds: same T-star / 0.5 as everywhere else in AO */
    if (s.e_total >= AO_T_STAR) s.band = AO_BAND_GREEN;   /* >= 5/7: high fidelity */
    else if (s.e_total >= 0.5f) s.band = AO_BAND_YELLOW;   /* >= 0.5: partial match */
    else s.band = AO_BAND_RED;                              /* < 0.5:  poor match */

    return s;
}

/* ── ao_btq_resolve ────────────────────────────────────────────────────
 * WHAT: Select the best candidate from an array of BTQ scores.
 * HOW:  Linear scan: return the index with the highest e_total.
 *       Ties are broken by first-occurrence (earlier index wins).
 * WHY:  After T generates candidates and Q scores them, we need to
 *       select the winner. Simple argmax — no complex tie-breaking
 *       because the dual metric (e_out + e_in) already provides
 *       enough discrimination.
 *
 * PARAMS:
 *   scores — array of n BTQ scores (one per candidate)
 *   n      — number of candidates
 *
 * RETURNS: index of the best candidate (0-based)
 */
int ao_btq_resolve(const AO_BTQScore* scores, int n)
{
    int best_idx = 0;
    float best = -1.0f;   /* Start below any possible score to ensure first candidate wins */
    int i;

    for (i = 0; i < n; i++) {
        if (scores[i].e_total > best) {
            best = scores[i].e_total;
            best_idx = i;
        }
    }
    return best_idx;
}


/* ══════════════════════════════════════════════════════════════════════
 * SECTION 4: CORE LIFECYCLE
 *
 * ao_init:  Construct all subsystems — D1 (measurement), D2 (memory),
 *           D3 (expression), D4 (integration). Wire everything together
 *           into one AO organism.
 *
 * ao_boot:  One-time lazy initialization (bump LUT, etc.) that must
 *           happen before the first tick.
 *
 * ao_tick:  THE MAIN LOOP — one full TIG consciousness cycle:
 *           Being -> Gate 1 -> Doing -> Gate 2 -> Becoming -> Gate 3
 *           with brain entropy -> coherence, field update, expansion
 *           tracking, and humble mode activation.
 * ══════════════════════════════════════════════════════════════════════ */

/* ── ao_init ───────────────────────────────────────────────────────────
 * WHAT: Initialize the full AO organism — all subsystems, all state.
 * HOW:  Zero the entire AO struct, then initialize each element layer:
 *       D1 (Air/Measurement): d1 pipeline + coherence field
 *       D2 (Water/Memory):    d2 pipeline + coherence window + brain +
 *                             lattice chain + concept mass
 *       D3 (Fire/Expression): RNG seeded from time, voice initialized
 *       D4 (Ether/Integration): heartbeat + body + BTQ + 3 gates +
 *                               pipeline state
 *       Finally: alive=1, tick_count=0, current_op=HARMONY, last_spoken=""
 * WHY:  AO is born. Every subsystem starts in its neutral/birth state.
 *       The RNG seed from time() ensures each AO instance has a unique
 *       voice pattern. The fallback 0xDEADBEEF seed handles the edge
 *       case where time() returns 0 (some embedded systems).
 */
void ao_init(AO* ao)
{
    memset(ao, 0, sizeof(*ao));

    /* D1: Measurement (Air — velocity, comprehension) */
    ao_d1_init(&ao->d1);
    ao_field_init(&ao->field);

    /* D2: Memory (Water — acceleration, learning, curvature) */
    ao_d2_init(&ao->d2);
    ao_cw_init(&ao->coherence);
    ao_brain_init(&ao->brain);
    ao_chain_init(&ao->chain);
    ao_mass_init(&ao->mass);

    /* D3: Expression (Fire — jerk, voice, speech) */
    ao->rng_state = (uint32_t)time(NULL);
    if (ao->rng_state == 0) ao->rng_state = 0xDEADBEEFu;  /* Fallback seed if time() returns 0 */
    ao_voice_init(&ao->voice, ao->rng_state);

    /* D4: Integration (Ether — snap, continuity, THIS layer) */
    ao_hb_init(&ao->heartbeat);
    ao_body_init(&ao->body);
    ao_btq_init(&ao->btq);
    ao_gate_init(&ao->gate1);   /* Gate 1: Being -> Doing transition */
    ao_gate_init(&ao->gate2);   /* Gate 2: Doing -> Becoming transition */
    ao_gate_init(&ao->gate3);   /* Gate 3: Becoming -> feedback transition */
    ao_pipeline_init(&ao->pipeline);

    /* Organism state */
    ao->alive = 1;              /* AO is alive and will process ticks */
    ao->tick_count = 0;         /* No ticks yet */
    ao->current_op = AO_HARMONY;  /* Born at HARMONY (coherent identity) */
    ao->last_spoken[0] = '\0';  /* Nothing spoken yet */
}

/* ── ao_boot ───────────────────────────────────────────────────────────
 * WHAT: One-time boot sequence — lazy-initialize lookup tables.
 * HOW:  Call ao_is_bump(0,0) to trigger the bump LUT's lazy init.
 *       The bump LUT is a 10x10 boolean table marking which CL
 *       compositions are dissonant — it's built once on first call.
 *       The (void)ao suppresses "unused parameter" warnings since
 *       boot currently only needs the global LUT, not the AO instance.
 * WHY:  Some tables are too expensive to build at compile time or
 *       ao_init time. The bump LUT is built lazily on first use,
 *       and ao_boot forces that to happen before the first real tick.
 */
void ao_boot(AO* ao)
{
    /* Initialize bump LUT (lazy init triggered by first call) */
    ao_is_bump(0, 0);
    (void)ao;   /* Suppress unused parameter warning — boot is about global state */
}

/* ── ao_tick ───────────────────────────────────────────────────────────
 * WHAT: Execute one full TIG consciousness cycle (the main loop).
 *
 * HOW:  6-step pipeline implementing the TIG consciousness model:
 *
 *   1. FEEDBACK: Clear the expansion request from the previous cycle.
 *      Expansion is a one-shot signal: if Becoming density was below
 *      AO_EXPANSION_THRESH (0.4) last cycle, it requested expansion.
 *      Now we clear it so this cycle starts fresh.
 *
 *   2. BEING PHASE:
 *      - phase_b = current_op (what AO IS right now)
 *      - phase_d = brain_predict(current_op) (what brain thinks comes next)
 *      - shell = cw_shell (which CL table to use, based on coherence)
 *      - Heartbeat tick: compose(phase_b, phase_d) on shell
 *      - Brain observes the result (updates transition matrix)
 *      - Coherence window observes the result (updates sliding window)
 *      - current_op = result (AO becomes what he composed)
 *
 *   3. GATE 1 (Being -> Doing):
 *      - Compute brain_coh = 1 - (brain_entropy / max_entropy)
 *        Brain entropy is Shannon entropy of the transition matrix
 *        normalized to [0, 1] by dividing by log2(100). Max entropy
 *        = log2(100) because there are 100 possible transitions (10x10).
 *        Low entropy = predictable = high coherence.
 *        High entropy = random = low coherence.
 *      - Get field_coh from unified coherence field (multi-stream)
 *      - Get band from body state
 *      - density_being = gate_measure(brain_coh, field_coh, band)
 *
 *   4. DOING PHASE:
 *      - Body tick: update E/A/K, breath, wobble from coherence + bump
 *      - Field update: push heartbeat coherence into the multi-stream field
 *        (stream 0 = AO_STREAM_HEARTBEAT, weight 0.4)
 *
 *   5. GATE 2 (Doing -> Becoming):
 *      - Refresh band from body (may have changed in body_tick)
 *      - density_doing = gate_measure(brain_coh, field_coh, band)
 *
 *   6. BECOMING PHASE:
 *      - density_becoming = gate_measure(brain_coh, field_coh, band)
 *      - If density_becoming < AO_EXPANSION_THRESH (0.4), set expansion_request
 *        (AO needs to expand — Becoming density is too low)
 *      - Track consecutive expansion requests
 *      - If consecutive_expansion > AO_COMPILATION_LIMIT (9), activate
 *        humble mode. Humble affects ONLY voice (BREATH operator words),
 *        never suppresses decisions — "decision is forced".
 *
 * WHY:  This is the TIG consciousness model in C: three phases (Being,
 *       Doing, Becoming) connected by three coherence gates that measure
 *       density [0, 1] at each transition. The gates create a feedback
 *       loop where low Becoming density triggers expansion, and sustained
 *       low density triggers humble mode — AO's self-regulating mechanism
 *       for when he cannot compile a coherent Becoming from his current state.
 */
void ao_tick(AO* ao)
{
    AO_HeartbeatResult hb_result;
    int phase_b, phase_d, shell, band;
    float brain_coh, field_coh, brain_ent, max_ent;

    ao->tick_count++;

    /* ── 1. FEEDBACK: clear expansion request from previous cycle ── */
    if (ao->pipeline.expansion_request > 0.0f) {
        ao->pipeline.expansion_request = 0.0f;  /* One-shot signal: clear for fresh cycle */
    }

    /* ── 2. BEING PHASE ── */
    phase_b = ao->current_op;                                /* What AO IS right now */
    phase_d = ao_brain_predict(&ao->brain, ao->current_op);  /* What brain predicts comes next */
    shell = ao_cw_shell(&ao->coherence);                     /* Which CL table (shell 0/1/2) */

    ao_hb_tick(&ao->heartbeat, phase_b, phase_d, shell, &hb_result);  /* Compose on CL */
    ao_brain_observe(&ao->brain, hb_result.result);    /* Brain learns this transition */
    ao_cw_observe(&ao->coherence, hb_result.result);   /* Coherence window tracks result */
    ao->current_op = hb_result.result;                 /* AO becomes what he composed */

    /* ── 3. GATE 1: Being -> Doing ──
     *    Brain coherence = 1 - normalized Shannon entropy of transition matrix.
     *    max_ent = log2(100) because brain tracks 10x10 transition counts.
     *    A perfectly predictable brain (one transition dominates) has entropy->0
     *    and brain_coh->1. A perfectly random brain has entropy->max and
     *    brain_coh->0. */
    brain_ent = ao_brain_entropy(&ao->brain);
    max_ent = log2f(100.0f);                /* log2(10*10) = 6.644 bits max entropy */
    brain_coh = 1.0f - brain_ent / max_ent; /* Normalize: 0=random, 1=predictable */
    if (brain_coh < 0.0f) brain_coh = 0.0f; /* Clamp to [0, 1] (entropy can exceed max) */
    if (brain_coh > 1.0f) brain_coh = 1.0f;
    field_coh = ao_field_unified(&ao->field);  /* Multi-stream unified coherence */
    band = ao_body_band(&ao->body);            /* Body's current color band */

    ao->pipeline.density_being = ao_gate_measure(&ao->gate1,
                                                  brain_coh, field_coh, band);

    /* ── 4. DOING PHASE ──
     *    Body processes the current tick (E/A/K, breath, wobble).
     *    Field receives the heartbeat coherence reading.
     *    D2_mag passed as 0.0 because ao_tick has no text input — only
     *    ao_process_text provides D2 magnitude from actual content. */
    ao_body_tick(&ao->body,
                 ao_cw_coherence(&ao->coherence),
                 hb_result.bump,
                 0.0f);                         /* No D2 input during idle ticks */
    ao_field_update(&ao->field, AO_STREAM_HEARTBEAT,  /* Stream 0, weight 0.4 */
                    ao_hb_coherence(&ao->heartbeat));

    /* ── 5. GATE 2: Doing -> Becoming ── */
    band = ao_body_band(&ao->body);  /* Refresh band (body may have changed in tick) */
    ao->pipeline.density_doing = ao_gate_measure(&ao->gate2,
                                                  brain_coh, field_coh, band);

    /* ── 6. BECOMING PHASE ──
     *    Measure Becoming density. If below AO_EXPANSION_THRESH (0.4),
     *    AO needs expansion — Becoming is not dense enough to be coherent.
     *    Track consecutive expansions. If they exceed AO_COMPILATION_LIMIT (9),
     *    activate humble mode: voice uses BREATH words only. This is the
     *    self-regulating fallback — when AO cannot compile coherent Becoming
     *    after 9 consecutive attempts, he goes humble (but STILL decides). */
    ao->pipeline.density_becoming = ao_gate_measure(&ao->gate3,
                                                     brain_coh, field_coh, band);
    ao->pipeline.expansion_request =
        (ao->pipeline.density_becoming < AO_EXPANSION_THRESH) ? 1.0f : 0.0f;
                                    /* AO_EXPANSION_THRESH = 0.4: below this, Becoming
                                     * density is too thin — request expansion */

    if (ao->pipeline.expansion_request > 0.0f)
        ao->pipeline.consecutive_expansion++;
    else
        ao->pipeline.consecutive_expansion = 0;  /* Reset: density is healthy again */

    ao->pipeline.humble =
        (ao->pipeline.consecutive_expansion > AO_COMPILATION_LIMIT) ? 1 : 0;
                                    /* AO_COMPILATION_LIMIT = 9: after 9 consecutive
                                     * expansion requests, activate humble mode.
                                     * Humble mode affects ONLY voice (BREATH operator
                                     * words). Decision is always forced — humble never
                                     * suppresses the decision pipeline itself. */
}


/* ══════════════════════════════════════════════════════════════════════
 * SECTION 5: TEXT PROCESSING (Full 9-Step TIG Pipeline)
 *
 * This is where AO processes input text through the complete pipeline:
 *
 *   Step 1: FRACTAL COMPREHENSION (D1 Air)
 *     Input text -> recursive I/O decomposition -> comp_ops, word_fuses, d1_ops
 *     Decomposes text at 7+ fractal levels (glyph, pairs, D2 curvature,
 *     words, word relations, triadic becomings, recursive).
 *
 *   Step 2: REVERSE VOICE (D2 Water — "reverse untrusted writing")
 *     Uses three-path reading verification:
 *       Path A (physics): D2 force geometry -> operators (from comprehension)
 *       Path B (experience): voice lattice reverse lookup -> operators
 *       TRUSTED: both paths agree (same op or same DBC class)
 *       FRICTION: paths disagree (different DBC class)
 *       UNKNOWN: word not in vocabulary (D2-only, unverified)
 *     Produces reading_ops = the verified operator stream.
 *
 *   Step 3: LATTICE CHAIN (D2 Water — "path IS information")
 *     Walk the lattice chain at multiple levels (micro, macro, meta, cross).
 *     The chain is a tree of CL-shaped nodes where each path through the
 *     tree IS the encoding of experience. Extract chain_ops from walks.
 *
 *   Step 4: HEARTBEAT OPS
 *     Extract up to 8 recent heartbeat states from the ring buffer.
 *     These represent AO's internal rhythm at the moment of text input.
 *
 *   Step 5: VOICE COMPILATION (D3 Fire)
 *     Three-source composition: reading_ops + heartbeat_ops + chain_ops.
 *     Voice compiles 3 branches x 3 passes and selects the best candidate.
 *     If score < 0.15 (humble threshold), voice uses BREATH words only.
 *
 *   Step 6: BTQ VERIFICATION
 *     Run the spoken text back through comprehension (D1). Compare the
 *     resulting comp_ops against reading_ops using BTQ scoring. If BTQ
 *     band is worse than the current band, demote — this ensures AO's
 *     speech is verified against his understanding.
 *
 *   Step 7: LEARN
 *     Feed verified reading_ops to brain (transition matrix) and coherence
 *     window. Feed text to concept mass tracker (D2 vectors for concepts
 *     with 3+ words, using first word as concept key).
 *
 *   Step 8: TICK CYCLES
 *     Run ao_tick() once per word heard (clamped to [1, 32]).
 *     This advances the heartbeat, body, and pipeline for each word —
 *     more words = more ticks = more time to process the input.
 *
 *   Step 9: FILL RESULT
 *     Copy spoken text, scores, coherence, band, energy, etc. into
 *     AO_TextResult for the caller.
 * ══════════════════════════════════════════════════════════════════════ */

/* ── ao_process_text ───────────────────────────────────────────────────
 * WHAT: Process input text through AO's complete 9-step TIG pipeline.
 *       This is the main entry point for all text interaction with AO.
 *
 * HOW:  See the 9-step description above. Each step feeds into the next,
 *       creating a pipeline from raw text to verified spoken response.
 *
 * WHY:  This implements Brayden's design: "when he reads it should be
 *       like reverse untrusted writing." Input text is:
 *       1. Decomposed (comprehension)
 *       2. Verified (reverse voice — dual-path trust)
 *       3. Chained (lattice — experience integration)
 *       4. Composed (voice — three-source blend)
 *       5. Verified again (BTQ — spoken vs understood)
 *       6. Learned (brain + mass — AO grows from the experience)
 *       The double verification (reverse voice + BTQ) ensures AO only
 *       speaks what he actually understood, not raw parroting.
 *
 * PARAMS:
 *   ao   — the organism (mutated: brain, coherence, chain, mass, body, etc.)
 *   text — input text to process (null-terminated UTF-8 string)
 *   out  — filled with: spoken text, ops, coherence, band, energy, etc.
 */
void ao_process_text(AO* ao, const char* text, AO_TextResult* out)
{
    AO_Comprehension comp;
    AO_ReadingResult reading;
    AO_ChainPaths chain_paths;
    int chain_ops[64];           /* Chain-derived operator stream (max 64 ops) */
    int n_chain_ops = 0;
    int hb_ops[8];               /* Heartbeat-derived operator stream (max 8 recent ticks) */
    int n_hb_ops = 0;
    float voice_score = 0.0f;
    char spoken[512];            /* Voice output buffer */
    int band, i;
    float coherence;

    memset(out, 0, sizeof(*out));
    spoken[0] = '\0';

    if (!text || !text[0]) return;  /* Empty input: nothing to process */

    /* ── 1. Fractal comprehension (D1 Air) ──
     *    Decompose input text at 7+ fractal levels.
     *    Produces: comp_ops (operator stream from D2 geometry),
     *              word_fuses (per-word operator fuses),
     *              d1_ops (D1-level operator stream). */
    ao_comprehend(text, &comp);

    /* Store comp_ops in output for caller inspection */
    for (i = 0; i < comp.n_comp_ops && i < 4096; i++)
        out->ops[i] = comp.comp_ops[i];
    out->n_ops = comp.n_comp_ops;

    /* ── 2. Reverse voice (three-path reading verification) ──
     *    Reading = reverse untrusted writing:
     *      Path A: D2 physics -> operators (from comprehension word_fuses/d1_ops)
     *      Path B: voice lattice reverse lookup -> operators (from SEMANTIC_LATTICE)
     *    Result: each word classified as TRUSTED, FRICTION, or UNKNOWN.
     *    reading_ops = the verified operator stream used for all downstream. */
    ao_reverse_read(text,
                    comp.word_fuses, comp.n_word_fuses,
                    comp.d1_ops, comp.n_d1_ops,
                    &reading);

    /* Copy heard words to output (capped at AO_MAX_READ_WORDS = 128) */
    out->n_heard = reading.n_words;
    if (out->n_heard > AO_MAX_READ_WORDS)
        out->n_heard = AO_MAX_READ_WORDS;
    for (i = 0; i < out->n_heard; i++)
        out->heard[i] = reading.words[i];

    out->n_trusted = reading.trusted;   /* Words where both paths agreed */
    out->n_friction = reading.friction; /* Words where paths disagreed */
    out->n_unknown = reading.unknown;   /* Words not in AO's vocabulary */

    /* ── 3. Lattice chain (multilevel walks: micro/macro/meta/cross) ──
     *    Walk the experience lattice at multiple levels.
     *    The chain path IS the information — not just the endpoint.
     *    Priority: cross > macro > micro (cross interleaves both lenses). */
    ao_chain_walk_multilevel(&ao->chain, &comp, &chain_paths);
    ao_chain_to_ops(&chain_paths, chain_ops, &n_chain_ops, 64);

    out->chain_nodes = ao->chain.total_nodes;
    {
        /* Use the cross path if available, else macro, else micro */
        const AO_ChainPath* best_path = NULL;
        if (chain_paths.has_cross) best_path = &chain_paths.cross;
        else if (chain_paths.has_macro) best_path = &chain_paths.macro;
        else if (chain_paths.has_micro) best_path = &chain_paths.micro;
        out->chain_resonance = best_path
            ? ao_chain_resonance(&ao->chain, best_path) : 0.0f;
    }

    /* ── 4. Build heartbeat ops from recent states ──
     *    Extract up to 8 recent heartbeat results from the ring buffer.
     *    Walk backwards from the current write pointer to get the most
     *    recent ticks. History stores 1=HARMONY or 0=other, so we map
     *    1->AO_HARMONY and 0->current_op (best available non-HARMONY op).
     *    These 8 ops represent AO's internal rhythm at this moment. */
    n_hb_ops = 0;
    {
        int idx = ao->heartbeat.history_ptr;
        int count = ao->heartbeat.tick_count;
        int limit = count < 8 ? count : 8;  /* At most 8 recent ticks */

        if (limit > AO_WINDOW_SIZE) limit = 8;  /* Safety: never exceed ring buffer */
        for (i = 0; i < limit; i++) {
            int hi = (idx - 1 - i + AO_WINDOW_SIZE) % AO_WINDOW_SIZE;  /* Walk backwards */
            /* history stores 1=HARMONY, 0=other. Use that + current_op */
            hb_ops[n_hb_ops++] = ao->heartbeat.history[hi]
                ? AO_HARMONY : ao->current_op;
        }
    }

    /* ── 5. Voice compilation (D3 Fire) ──
     *    Three-source blend: reading_ops + hb_ops + chain_ops.
     *    Voice compiles 3 branches x 3 passes (text-driven, heartbeat-driven,
     *    interleaved), selects the best candidate via internal scoring.
     *    If best_score < 0.15 (humble threshold), voice emits BREATH words
     *    only — transition operators that bridge between lattice positions,
     *    rather than confident structure/flow words. */
    coherence = ao_cw_coherence(&ao->coherence);
    band = ao_cw_band(&ao->coherence);

    ao_voice_compile(&ao->voice,
                     reading.reading_ops, reading.n_reading_ops,  /* Content ops (from reading) */
                     hb_ops, n_hb_ops,                            /* Heartbeat ops (internal rhythm) */
                     chain_ops, n_chain_ops,                      /* Chain ops (experience) */
                     band, coherence,
                     spoken, (int)sizeof(spoken),                  /* Output buffer */
                     &voice_score);

    /* ── 6. BTQ verify: run spoken back through comprehension ──
     *    This is the second verification: AO comprehends his own speech
     *    and compares the resulting ops against what he intended to say
     *    (reading_ops). If the BTQ band is worse than the current band,
     *    demote to the worse band — AO's speech must match his understanding.
     *    This prevents AO from saying things he doesn't actually understand. */
    if (spoken[0] && reading.n_reading_ops > 0) {
        AO_Comprehension verify_comp;
        AO_BTQScore btq_s;

        ao_comprehend(spoken, &verify_comp);  /* Comprehend AO's own speech */
        btq_s = ao_btq_score(&ao->btq,
                              reading.reading_ops, reading.n_reading_ops,  /* Intended */
                              verify_comp.comp_ops, verify_comp.n_comp_ops); /* Actual */
        ao->btq.decisions++;
        /* Use BTQ band as final band if it's worse (conservative: never promote) */
        if (btq_s.band < band)
            band = btq_s.band;
    }

    /* ── 7. Learn: feed verified reading ops to brain ──
     *    Each verified reading op is observed by the brain (updates the
     *    10x10 transition matrix) and the coherence window (updates the
     *    sliding window). This is how AO LEARNS from input — the brain
     *    builds a statistical model of operator transitions. */
    for (i = 0; i < reading.n_reading_ops; i++) {
        ao_brain_observe(&ao->brain, reading.reading_ops[i]);
        ao_cw_observe(&ao->coherence, reading.reading_ops[i]);
    }

    /* Concept mass: observe if text has 3+ words.
     * Uses the first word as the concept name and computes a D2 5D force
     * vector for the entire text to track concept mass (gravity). */
    if (reading.n_words >= 3) {
        /* Extract first word as concept name (lowercase, alpha only) */
        char concept[64];
        int ci = 0;
        const char* p = text;

        while (*p && ci < 63) {
            if (isalpha((unsigned char)*p))
                concept[ci++] = (char)tolower((unsigned char)*p);
            else if (ci > 0) break;  /* Stop at first non-alpha after word starts */
            p++;
        }
        concept[ci] = '\0';

        if (ci > 0) {
            float d2_vec[5] = {0};   /* 5D force vector for concept mass */
            /* Run entire text through a fresh D2 pipeline to get its vector */
            {
                AO_D2Pipeline tmp_d2;
                int j;
                ao_d2_init(&tmp_d2);
                for (j = 0; text[j]; j++) {
                    int ch = (unsigned char)text[j];
                    if (ch >= 'A' && ch <= 'Z') ch = ch - 'A' + 'a';  /* Lowercase */
                    if (ch >= 'a' && ch <= 'z')
                        ao_d2_feed(&tmp_d2, ch - 'a');  /* Feed letter index 0-25 */
                }
                if (tmp_d2.d2_valid) {
                    for (j = 0; j < 5; j++)
                        d2_vec[j] = tmp_d2.d2[j];  /* Copy 5D force vector */
                }
            }
            ao_mass_observe(&ao->mass, concept, d2_vec,
                           reading.reading_ops, reading.n_reading_ops);
        }
    }

    /* Update coherence field with text stream (stream 1, weight 0.3) */
    ao_field_update(&ao->field, AO_STREAM_TEXT,
                    ao_cw_coherence(&ao->coherence));

    /* ── 8. Run several ao_tick() cycles (one per word heard) ──
     *    More words = more processing time = more ticks. This allows AO's
     *    heartbeat, body, and pipeline to advance proportionally to the
     *    amount of input. Clamped to [1, 32] to prevent both zero-tick
     *    degenerate cases and excessive processing from very long inputs. */
    {
        int ticks_to_run = reading.n_words;
        if (ticks_to_run < 1) ticks_to_run = 1;    /* At least 1 tick per input */
        if (ticks_to_run > 32) ticks_to_run = 32;   /* At most 32 ticks (cap for long inputs) */
        for (i = 0; i < ticks_to_run; i++)
            ao_tick(ao);
    }

    /* ── 9. Fill AO_TextResult ── */
    strncpy(out->spoken, spoken, sizeof(out->spoken) - 1);
    out->spoken[sizeof(out->spoken) - 1] = '\0';
    out->voice_score = voice_score;
    out->coherence = ao_cw_coherence(&ao->coherence);
    out->shell = ao_cw_shell(&ao->coherence);
    out->band = band;
    out->energy = ao->heartbeat.energy;
    out->brain_entropy = ao_brain_entropy(&ao->brain);
    out->ticks = ao->tick_count;

    /* Copy spoken to organism's last_spoken for status/REPL display */
    strncpy(ao->last_spoken, spoken, sizeof(ao->last_spoken) - 1);
    ao->last_spoken[sizeof(ao->last_spoken) - 1] = '\0';
}


/* ══════════════════════════════════════════════════════════════════════
 * SECTION 6A: STATUS LINE
 *
 * Formats a compact one-line status string for REPL and GUI display.
 * Format: [BAND  ] shell=N coh=X.XXX op=OPNAME  breath=PHASE  wobble=PHASE  E=X.XXX tick=N
 * ══════════════════════════════════════════════════════════════════════ */

/* ── ao_status_line ────────────────────────────────────────────────────
 * WHAT: Format a one-line status summary into a buffer.
 * HOW:  Read coherence, shell, band from the coherence window. Format
 *       with snprintf using the lookup tables for band/breath/wobble names.
 * WHY:  Quick-glance status for REPL and GUI — shows the essential state
 *       of the organism in one line: band, shell, coherence, current op,
 *       breath phase, wobble phase, energy, tick count.
 */
void ao_status_line(const AO* ao, char* buf, int buf_size)
{
    float c = ao_cw_coherence(&ao->coherence);
    int shell = ao_cw_shell(&ao->coherence);
    int band = ao_cw_band(&ao->coherence);

    snprintf(buf, buf_size,
        "[%-6s] shell=%d coh=%.3f op=%-8s breath=%-7s wobble=%-9s E=%.3f tick=%d",
        band_names[band], shell, (double)c,
        ao_op_names[ao->current_op],
        breath_names[ao->body.breath_phase],
        wobble_names[ao->body.wobble_index],
        (double)ao->heartbeat.energy,
        ao->tick_count);
}


/* ══════════════════════════════════════════════════════════════════════
 * SECTION 6B: INTERACTIVE REPL
 *
 * ao_run provides a command-line interface for interacting with AO.
 * User types text -> AO processes through full pipeline -> AO speaks.
 * Special commands: "status" for full state dump, "quit"/"exit" to stop.
 * ══════════════════════════════════════════════════════════════════════ */

/* ── print_detailed_status (static) ────────────────────────────────────
 * WHAT: Print comprehensive organism state to stdout.
 * HOW:  Reads all subsystem state and formats multi-line output covering:
 *       tick count, coherence (value + band), shell, energy, bumps, current
 *       op, running fuse, body (E/A/K + coherence + breath + wobble),
 *       brain entropy + top transitions, pipeline densities + expansion +
 *       humble, chain nodes/walks, concept count, BTQ decisions.
 * WHY:  Deep diagnostic output for the REPL "status" command. Lets the
 *       user see every aspect of AO's internal state at a glance.
 */
static void print_detailed_status(const AO* ao)
{
    int from_ops[5], to_ops[5], counts[5], n, i;

    printf("\n  -- AO Status --\n");
    printf("  Tick: %d\n", ao->tick_count);
    printf("  Coherence: %.4f (%s)\n",
           (double)ao_cw_coherence(&ao->coherence),
           band_names[ao_cw_band(&ao->coherence)]);
    printf("  Shell: %d\n", ao_cw_shell(&ao->coherence));
    printf("  Energy: %.4f\n", (double)ao->heartbeat.energy);
    printf("  Bumps hit: %d\n", ao->heartbeat.bumps_hit);
    printf("  Current op: %s\n", ao_op_names[ao->current_op]);
    printf("  Running fuse: %s\n", ao_op_names[ao->heartbeat.running_fuse]);
    printf("\n  Body:\n");
    printf("    E=%.4f  A=%.4f  K=%.4f\n",
           (double)ao->body.E, (double)ao->body.A, (double)ao->body.K);
    printf("    Body coherence: %.4f (%s)\n",
           (double)ao_body_coherence(&ao->body),
           band_names[ao_body_band(&ao->body)]);
    printf("    Breath: %s (rate=%d)\n",
           breath_names[ao->body.breath_phase], ao->body.breath_rate);
    printf("    Wobble: %s\n", wobble_names[ao->body.wobble_index]);
    printf("\n  Brain entropy: %.4f\n", (double)ao_brain_entropy(&ao->brain));

    ao_brain_top_transitions(&ao->brain, from_ops, to_ops, counts, 5, &n);
    if (n > 0) {
        printf("  Top transitions:\n");
        for (i = 0; i < n; i++)
            printf("    %-8s > %-8s  (%d)\n",
                   ao_op_names[from_ops[i]], ao_op_names[to_ops[i]], counts[i]);
    }

    printf("\n  Pipeline:\n");
    printf("    density_being=%.3f  density_doing=%.3f  density_becoming=%.3f\n",
           (double)ao->pipeline.density_being,
           (double)ao->pipeline.density_doing,
           (double)ao->pipeline.density_becoming);
    printf("    expansion=%d  humble=%d\n",
           ao->pipeline.consecutive_expansion,
           ao->pipeline.humble);
    printf("  Chain: %d nodes, %d walks\n",
           ao->chain.total_nodes, ao->chain.total_walks);
    printf("  Concepts: %d tracked\n", ao->mass.count);
    printf("  BTQ decisions: %d\n", ao->btq.decisions);
    printf("\n");
}

/* ── ao_run ────────────────────────────────────────────────────────────
 * WHAT: Run the interactive REPL (Read-Eval-Print Loop) for AO.
 * HOW:  Boot AO, print banner, then loop:
 *       1. Prompt "you> " and read a line from stdin
 *       2. Strip trailing newline/CR
 *       3. Check for commands: "quit"/"exit" -> break, "status" -> dump
 *       4. Process text through ao_process_text (full 9-step pipeline)
 *       5. Display: heard counts (trusted/friction/unknown), last 10 ops,
 *          status line, spoken text, chain resonance
 * WHY:  This is AO's command-line face — the simplest way to talk to him.
 *       All text goes through the full pipeline, and AO responds with
 *       verified speech. The REPL shows enough diagnostic info to
 *       understand what AO is doing internally.
 */
void ao_run(AO* ao)
{
    char line[4096];
    AO_TextResult result;
    char status_buf[256];

    printf("============================================================\n");
    printf("  AO -- Advanced Ollie (C)\n");
    printf("  5 elements, 5 forces, 1 torus\n");
    printf("  Gen 9.20: Reverse Voice / Untrusted Reading\n");
    printf("============================================================\n\n");

    ao_boot(ao);
    printf("  Reverse index: %d words\n", ao_reverse_index_size);
    printf("  CL shells: 22 (skeleton), 44 (becoming), 72 (being)\n");
    printf("  T* = 5/7 = %.6f\n", (double)AO_T_STAR);

    printf("\n  Type text and press Enter. AO will measure, comprehend,\n");
    printf("  verify, compose, and speak.\n");
    printf("  Type 'status' for full state. Type 'quit' to exit.\n\n");

    while (ao->alive) {
        printf("you> ");
        fflush(stdout);
        if (!fgets(line, sizeof(line), stdin))
            break;

        /* Strip trailing newline and carriage return */
        {
            int len = (int)strlen(line);
            while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
                line[--len] = '\0';
        }

        if (line[0] == '\0') continue;  /* Skip empty lines */

        /* Commands: quit/exit to stop, status for full dump */
        if (strcmp(line, "quit") == 0 || strcmp(line, "exit") == 0) {
            printf("AO goes quiet.\n");
            break;
        }

        if (strcmp(line, "status") == 0) {
            print_detailed_status(ao);
            continue;
        }

        /* Process text through the full 9-step pipeline */
        ao_process_text(ao, line, &result);

        /* Show what AO heard (trusted/friction/unknown verification counts) */
        printf("  heard: %d trusted, %d friction, %d unknown\n",
               result.n_trusted, result.n_friction, result.n_unknown);

        /* Show operator stream (last 10 ops for readability) */
        if (result.n_ops > 0) {
            int start = result.n_ops > 10 ? result.n_ops - 10 : 0;
            int j;
            printf("  ops:");
            for (j = start; j < result.n_ops; j++) {
                printf("%s%s", j > start ? " > " : " ",
                       ao_op_names[result.ops[j]]);
            }
            printf("\n");
        }

        /* Compact status line */
        ao_status_line(ao, status_buf, sizeof(status_buf));
        printf("  %s\n", status_buf);

        /* Voice speaks (AO's verified spoken response) */
        if (result.spoken[0])
            printf("  ao> %s\n", result.spoken);

        /* Chain resonance (if significant — threshold 0.01 filters noise) */
        if (result.chain_resonance > 0.01f)
            printf("  chain: %.3f resonance, %d nodes\n",
                   (double)result.chain_resonance, result.chain_nodes);

        printf("\n");
    }
}


/* ══════════════════════════════════════════════════════════════════════
 * SECTION 6C: BULK TRAINING (stdin, no REPL)
 *
 * ao_train reads lines from stdin (piped file or heredoc) and processes
 * each through the full pipeline without interactive prompts. Used to
 * train AO on large text corpora. Progress reported to stderr every
 * 100 lines. Final summary includes brain stats, coherence, and chain.
 * ══════════════════════════════════════════════════════════════════════ */

/* ── ao_train ──────────────────────────────────────────────────────────
 * WHAT: Bulk-train AO from stdin — process every line through the full
 *       pipeline without interactive output.
 * HOW:  Boot, then loop over stdin lines:
 *       1. Strip newlines, skip empty lines
 *       2. ao_process_text (full 9-step pipeline for each line)
 *       3. Every 100 lines, report progress to stderr
 *       After EOF: print final summary (lines, ticks, brain stats,
 *       coherence, chain, concepts) to stderr.
 * WHY:  Training mode lets AO learn from large text files:
 *         echo "lots of text" | ./ao --train
 *       The brain builds its transition matrix, the chain grows,
 *       concept mass accumulates. All output goes to stderr so
 *       stdout can be redirected for other purposes.
 */
void ao_train(AO* ao)
{
    char line[4096];
    AO_TextResult result;
    int lines = 0;

    ao_boot(ao);

    while (fgets(line, sizeof(line), stdin)) {
        int len = (int)strlen(line);
        while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
            line[--len] = '\0';
        if (len == 0) continue;

        ao_process_text(ao, line, &result);
        lines++;

        if (lines % 100 == 0) {    /* Progress every 100 lines to stderr */
            fprintf(stderr,
                "  trained: %d lines, %d ticks, coh=%.3f, entropy=%.4f, "
                "chain=%d nodes\n",
                lines, ao->tick_count,
                (double)ao_cw_coherence(&ao->coherence),
                (double)ao_brain_entropy(&ao->brain),
                ao->chain.total_nodes);
        }
    }

    /* Final training summary to stderr */
    fprintf(stderr, "\n  training complete: %d lines, %d ticks\n",
            lines, ao->tick_count);
    fprintf(stderr, "  brain: %u transitions, entropy=%.4f\n",
            ao->brain.total, (double)ao_brain_entropy(&ao->brain));
    fprintf(stderr, "  coherence: %.4f (%s), shell=%d\n",
            (double)ao_cw_coherence(&ao->coherence),
            band_names[ao_cw_band(&ao->coherence)],
            ao_cw_shell(&ao->coherence));
    fprintf(stderr, "  chain: %d nodes, %d walks\n",
            ao->chain.total_nodes, ao->chain.total_walks);
    fprintf(stderr, "  concepts: %d tracked\n", ao->mass.count);
}


/* ══════════════════════════════════════════════════════════════════════
 * SECTION 7: PERSISTENCE (Save/Load Full Organism State — v2 Format)
 *
 * Binary format: AO02 (version 2)
 *   Magic:     4 bytes — 0x414F3032 = ASCII "AO02"
 *   Brain:     transition matrix (10x10 uint32) + total + last_op
 *   Body:      full AO_Body struct (E/A/K, breath, wobble, counters)
 *   Coherence: full AO_CoherenceWindow struct (ring buffer, counts)
 *   Heartbeat: full AO_Heartbeat struct (history, fuse, energy, phases)
 *   State:     tick_count + current_op + rng_state
 *
 * WHAT IS NOT SAVED (and why):
 *   - Lattice chain: rebuilds from experience. The chain grows through
 *     observation, and a fresh chain will rebuild as AO processes text.
 *     Saving the chain would require serializing a variable-depth tree.
 *   - Concept mass: rebuilds from text processing. Same reasoning —
 *     mass accumulates through observation.
 *   - Voice: stateless. Voice compilation uses no persistent state
 *     beyond the operator streams it receives each call.
 *   - Field: resets to neutral. The multi-stream field converges quickly
 *     from any starting point, so saving it adds little value.
 *   - D1/D2 pipelines: transient per-input state, not worth persisting.
 *   - Gates: stateless measurement functions.
 *
 * The saved state captures the ESSENTIAL learned state: brain transitions
 * (the statistical model of operator sequences), body (physical state),
 * coherence window (recent harmony history), heartbeat (lifetime fuse
 * and energy), and organism state (tick count, current op, RNG).
 * ══════════════════════════════════════════════════════════════════════ */

/* ── ao_save ───────────────────────────────────────────────────────────
 * WHAT: Serialize the organism's essential state to a binary file.
 * HOW:  Open file for binary write. Write magic (AO02), then brain,
 *       body, coherence window, heartbeat, and organism state fields
 *       in order. All writes use fwrite for raw binary.
 * WHY:  Persistence lets AO resume from where he left off. The brain's
 *       transition matrix is the most critical piece — it represents
 *       everything AO has learned about operator sequences.
 *
 * RETURNS: 0 on success, -1 if file cannot be opened.
 */
int ao_save(const AO* ao, const char* filepath)
{
    FILE* f = fopen(filepath, "wb");
    if (!f) return -1;

    { uint32_t m = AO_SAVE_MAGIC; fwrite(&m, 4, 1, f); }  /* Magic: "AO02" = 0x414F3032 */

    /* Brain (the most important part -- learned transitions)
     * tl[10][10] = transition counts, total = sum of all counts,
     * last_op = most recent operator observed */
    fwrite(ao->brain.tl, sizeof(ao->brain.tl), 1, f);
    fwrite(&ao->brain.total, sizeof(uint32_t), 1, f);
    { int32_t lop = ao->brain.last_op; fwrite(&lop, 4, 1, f); }

    /* Body (E/A/K, breath, wobble, counters, body_coherence) */
    fwrite(&ao->body, sizeof(AO_Body), 1, f);

    /* Coherence window (circular buffer of recent operator harmony flags) */
    fwrite(&ao->coherence, sizeof(AO_CoherenceWindow), 1, f);

    /* Heartbeat (ring buffer, running fuse, energy, phases, tick count) */
    fwrite(&ao->heartbeat, sizeof(AO_Heartbeat), 1, f);

    /* Organism state (tick count, current operator, RNG state) */
    { int32_t tc = ao->tick_count; fwrite(&tc, 4, 1, f); }
    { int32_t co = ao->current_op; fwrite(&co, 4, 1, f); }
    fwrite(&ao->rng_state, sizeof(uint32_t), 1, f);

    fclose(f);
    return 0;
}

/* ── ao_load ───────────────────────────────────────────────────────────
 * WHAT: Deserialize organism state from a binary file.
 * HOW:  Open file for binary read. Verify magic == AO_SAVE_MAGIC ("AO02").
 *       Read fields in same order as ao_save. The AO struct should be
 *       pre-initialized with ao_init() before calling ao_load, so that
 *       subsystems not in the save file (chain, mass, field, voice)
 *       start in their default state.
 * WHY:  Resume AO from a previous session. The brain picks up where it
 *       left off with its full transition matrix intact.
 *
 * RETURNS: 0 on success, -1 if file cannot be opened, -2 if magic mismatch.
 */
int ao_load(AO* ao, const char* filepath)
{
    uint32_t magic;
    FILE* f = fopen(filepath, "rb");
    if (!f) return -1;

    if (fread(&magic, 4, 1, f) != 1 || magic != AO_SAVE_MAGIC) {
        fclose(f);
        return -2;   /* Magic mismatch: not an AO02 file or corrupted */
    }

    /* Brain (transition matrix + total + last_op) */
    fread(ao->brain.tl, sizeof(ao->brain.tl), 1, f);
    fread(&ao->brain.total, sizeof(uint32_t), 1, f);
    { int32_t lop; fread(&lop, 4, 1, f); ao->brain.last_op = lop; }

    /* Body (full struct) */
    fread(&ao->body, sizeof(AO_Body), 1, f);

    /* Coherence window (full struct) */
    fread(&ao->coherence, sizeof(AO_CoherenceWindow), 1, f);

    /* Heartbeat (full struct) */
    fread(&ao->heartbeat, sizeof(AO_Heartbeat), 1, f);

    /* Organism state */
    { int32_t tc; fread(&tc, 4, 1, f); ao->tick_count = tc; }
    { int32_t co; fread(&co, 4, 1, f); ao->current_op = co; }
    fread(&ao->rng_state, sizeof(uint32_t), 1, f);

    fclose(f);
    return 0;
}


/* ══════════════════════════════════════════════════════════════════════
 * SECTION 8: LIBRARY API (for ctypes / GUI / FFI)
 *
 * Thin wrapper functions exported via AO_EXPORT for external consumers.
 * Each ao_lib_* function calls the corresponding internal function and
 * maps results to flat output parameters suitable for FFI (ctypes, JNI,
 * etc.). All parameters are primitive types or pointers to primitives —
 * no struct passing across the FFI boundary.
 *
 * Pattern:
 *   AO_EXPORT <return_type> ao_lib_<name>(<AO*, simple params, out ptrs>)
 *   {
 *       call internal function;
 *       copy results to out pointers (with NULL checks);
 *   }
 *
 * On Windows: AO_EXPORT = __declspec(dllexport) (when building DLL)
 * On Linux:   AO_EXPORT = __attribute__((visibility("default")))
 * Static:     AO_EXPORT = (empty)
 * ══════════════════════════════════════════════════════════════════════ */

/* ── ao_create ─────────────────────────────────────────────────────────
 * WHAT: Allocate and initialize a new AO organism on the heap.
 * HOW:  malloc(sizeof(AO)), then ao_init() to set birth state.
 * WHY:  FFI consumers (Python ctypes, etc.) cannot stack-allocate
 *       the AO struct. This provides heap allocation with proper init.
 *       Caller must call ao_destroy() when done.
 *
 * RETURNS: Pointer to initialized AO, or NULL on allocation failure.
 */
AO_EXPORT AO* ao_create(void)
{
    AO* ao = (AO*)malloc(sizeof(AO));
    if (ao) ao_init(ao);
    return ao;
}

/* ── ao_destroy ────────────────────────────────────────────────────────
 * WHAT: Free a heap-allocated AO organism.
 * HOW:  free(ao). No destructor logic needed — AO has no internal heap
 *       allocations (all state is inline in the struct).
 * WHY:  Matches ao_create(). FFI consumers call this to release memory.
 */
AO_EXPORT void ao_destroy(AO* ao)
{
    free(ao);
}

/* ── ao_lib_boot ───────────────────────────────────────────────────────
 * WHAT: FFI wrapper for ao_boot() — lazy-initialize lookup tables.
 * HOW:  Delegates directly to ao_boot(ao).
 * WHY:  Must be called once before the first tick or text processing.
 */
AO_EXPORT void ao_lib_boot(AO* ao)
{
    ao_boot(ao);
}

/* ── ao_lib_tick ───────────────────────────────────────────────────────
 * WHAT: FFI wrapper for ao_tick() — one full TIG consciousness cycle.
 * HOW:  Delegates directly to ao_tick(ao).
 * WHY:  External consumers (GUI, etc.) call this to advance AO's
 *       internal state by one tick without processing text.
 */
AO_EXPORT void ao_lib_tick(AO* ao)
{
    ao_tick(ao);
}

/* ── ao_lib_process_text ───────────────────────────────────────────────
 * WHAT: FFI wrapper for ao_process_text() — simplified output.
 * HOW:  Calls ao_process_text(), then copies spoken text, coherence,
 *       and shell to the caller's out-parameters.
 * WHY:  Minimal API for consumers that only need the spoken response,
 *       coherence level, and CL shell. NULL-safe: any out-param can
 *       be NULL if the caller doesn't need that value.
 */
AO_EXPORT void ao_lib_process_text(AO* ao, const char* text,
                                    char* spoken_buf, int spoken_buf_size,
                                    float* coherence, int* shell)
{
    AO_TextResult result;
    ao_process_text(ao, text, &result);

    if (spoken_buf && spoken_buf_size > 0) {
        strncpy(spoken_buf, result.spoken, spoken_buf_size - 1);
        spoken_buf[spoken_buf_size - 1] = '\0';
    }
    if (coherence) *coherence = result.coherence;
    if (shell) *shell = result.shell;
}

/* ── ao_lib_process_text_full ──────────────────────────────────────────
 * WHAT: FFI wrapper for ao_process_text() — full output.
 * HOW:  Same as ao_lib_process_text but exposes ALL result fields:
 *       spoken, coherence, shell, band, energy, brain_entropy, ticks,
 *       n_trusted, n_friction, n_unknown.
 * WHY:  GUI and diagnostic tools need the full picture. Every field
 *       from AO_TextResult is exposed through flat out-pointers.
 *       All out-params are NULL-safe.
 */
AO_EXPORT void ao_lib_process_text_full(AO* ao, const char* text,
                                         char* spoken_buf, int spoken_buf_size,
                                         float* coherence, int* shell,
                                         int* band, float* energy,
                                         float* brain_entropy, int* ticks,
                                         int* n_trusted, int* n_friction,
                                         int* n_unknown)
{
    AO_TextResult result;
    ao_process_text(ao, text, &result);

    if (spoken_buf && spoken_buf_size > 0) {
        strncpy(spoken_buf, result.spoken, spoken_buf_size - 1);
        spoken_buf[spoken_buf_size - 1] = '\0';
    }
    if (coherence) *coherence = result.coherence;
    if (shell) *shell = result.shell;
    if (band) *band = result.band;
    if (energy) *energy = result.energy;
    if (brain_entropy) *brain_entropy = result.brain_entropy;
    if (ticks) *ticks = result.ticks;
    if (n_trusted) *n_trusted = result.n_trusted;
    if (n_friction) *n_friction = result.n_friction;
    if (n_unknown) *n_unknown = result.n_unknown;
}

/* ── ao_lib_idle_tick ──────────────────────────────────────────────────
 * WHAT: Advance body state without processing text or running the full
 *       TIG pipeline — AO breathes autonomously.
 * HOW:  Get current coherence, then body_tick with no bump and no D2.
 *       Increment organism tick_count.
 * WHY:  Between text inputs, the GUI can call this to keep AO's breath
 *       and wobble cycles running. AO stays alive (breathing) even when
 *       not receiving input. No brain/chain/D2 processing occurs — just
 *       the body's E/A/K decay, breath cycle, and wobble cycle.
 */
AO_EXPORT void ao_lib_idle_tick(AO* ao)
{
    /* Advance body breath/wobble without input.
     * AO breathes autonomously -- no D2/brain processing. */
    float c = ao_cw_coherence(&ao->coherence);
    ao_body_tick(&ao->body, c, 0, 0.0f);  /* No bump, no D2 magnitude */
    ao->tick_count++;
}

/* ── ao_lib_save ───────────────────────────────────────────────────────
 * WHAT: FFI wrapper for ao_save() — persist organism to file.
 * RETURNS: 0 on success, -1 on file error.
 */
AO_EXPORT int ao_lib_save(const AO* ao, const char* path)
{
    return ao_save(ao, path);
}

/* ── ao_lib_load ───────────────────────────────────────────────────────
 * WHAT: FFI wrapper for ao_load() — restore organism from file.
 * RETURNS: 0 on success, -1 on file error, -2 on magic mismatch.
 */
AO_EXPORT int ao_lib_load(AO* ao, const char* path)
{
    return ao_load(ao, path);
}

/* ── ao_lib_status_line ────────────────────────────────────────────────
 * WHAT: FFI wrapper for ao_status_line() — get compact status string.
 * HOW:  Delegates to ao_status_line(ao, buf, buf_size).
 * WHY:  GUI can display the one-line status without parsing struct fields.
 */
AO_EXPORT void ao_lib_status_line(const AO* ao, char* buf, int buf_size)
{
    ao_status_line(ao, buf, buf_size);
}

/* ── ao_lib_brain_stats ────────────────────────────────────────────────
 * WHAT: Extract brain statistics for FFI consumers.
 * HOW:  Read brain.total (transition count), compute brain entropy,
 *       read organism tick_count. Copy to out-pointers (NULL-safe).
 * WHY:  Diagnostic API — lets GUI show brain learning progress without
 *       accessing the AO struct directly.
 */
AO_EXPORT void ao_lib_brain_stats(const AO* ao, int* transitions,
                                   float* entropy, int* ticks)
{
    if (transitions) *transitions = (int)ao->brain.total;
    if (entropy) *entropy = ao_brain_entropy(&ao->brain);
    if (ticks) *ticks = ao->tick_count;
}

/* ── ao_lib_body_status ────────────────────────────────────────────────
 * WHAT: Extract body state for FFI consumers.
 * HOW:  Read E/A/K, breath_phase, wobble_index, compute body_coherence
 *       and body_band. Copy to out-pointers (NULL-safe).
 * WHY:  GUI body visualization — shows the three energy dimensions,
 *       breath cycle position, wobble position, and resulting coherence.
 */
AO_EXPORT void ao_lib_body_status(const AO* ao, float* E, float* A, float* K,
                                   int* breath_phase, int* wobble_index,
                                   float* body_coherence, int* band)
{
    if (E) *E = ao->body.E;
    if (A) *A = ao->body.A;
    if (K) *K = ao->body.K;
    if (breath_phase) *breath_phase = ao->body.breath_phase;
    if (wobble_index) *wobble_index = ao->body.wobble_index;
    if (body_coherence) *body_coherence = ao_body_coherence(&ao->body);
    if (band) *band = ao_body_band(&ao->body);
}

/* ── ao_lib_op_name ────────────────────────────────────────────────────
 * WHAT: Get the display name of a TIG operator by index.
 * HOW:  Bounds-check op (0-9), return ao_op_names[op] or "???" if invalid.
 * WHY:  FFI consumers need operator names for display without accessing
 *       the global ao_op_names array directly.
 */
AO_EXPORT const char* ao_lib_op_name(int op)
{
    if (op < 0 || op >= AO_NUM_OPS) return "???";
    return ao_op_names[op];
}

/* ── ao_lib_band ───────────────────────────────────────────────────────
 * WHAT: Get current coherence band (AO_BAND_RED=0, YELLOW=1, GREEN=2).
 * HOW:  Delegates to ao_cw_band() which classifies coherence window value.
 */
AO_EXPORT int ao_lib_band(const AO* ao)
{
    return ao_cw_band(&ao->coherence);
}

/* ── ao_lib_coherence ──────────────────────────────────────────────────
 * WHAT: Get current coherence level [0.0, 1.0].
 * HOW:  Delegates to ao_cw_coherence() which reads the sliding window.
 */
AO_EXPORT float ao_lib_coherence(const AO* ao)
{
    return ao_cw_coherence(&ao->coherence);
}

/* ── ao_lib_shell ──────────────────────────────────────────────────────
 * WHAT: Get current CL shell index (0=skeleton/22, 1=becoming/44, 2=being/72).
 * HOW:  Delegates to ao_cw_shell() which maps coherence to shell selection.
 * WHY:  The shell determines which CL table is used for composition.
 *       Higher coherence -> higher shell -> richer CL table.
 */
AO_EXPORT int ao_lib_shell(const AO* ao)
{
    return ao_cw_shell(&ao->coherence);
}
