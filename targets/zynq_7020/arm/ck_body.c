/*
 * ck_body.c -- CK's Body Rhythms on ARM (Bare Metal)
 * ====================================================
 * Operator: BREATH (8) -- the body breathes with CK.
 *
 * Port of ck_body.py to bare metal C.
 * Three interlocking rhythms that drive everything:
 *   Heartbeat: E/A/K triad → coherence → band classification
 *   Breath:    4-phase cycle, fractal time compression
 *   Pulse:     Information flow gated by breath
 *
 * Key insight from ck_body.py:
 *   When falling (C < T*/2), breath COMPRESSES (2 beats/cycle)
 *   but dreams INTENSIFY (5 per beat, depth 8).
 *   More exploration in less time. Finding paths before lock-in.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

#include "ck_body.h"
#include "ck_brain.h"   /* operator constants */
#include <string.h>
#include <math.h>

/* ── Heartbeat ── */

static void heartbeat_init(CK_Heartbeat* hb) {
    hb->E = 0.0f;
    hb->A = 0.3f;
    hb->K = 0.5f;
    hb->C = 0.0f;
    hb->band = CK_BAND_YELLOW;
    hb->phase = 0;  /* Start at B (Being) */
    hb->E_decay = 0.95f;
    hb->A_decay = 0.98f;
    hb->K_grow = 0.01f;
    hb->ticks = 0;
}

static void heartbeat_calc_coherence(CK_Heartbeat* hb) {
    /* C = (1-E) * (1-A) * max(K, 0.1) */
    float k_safe = (hb->K > 0.1f) ? hb->K : 0.1f;
    hb->C = (1.0f - hb->E) * (1.0f - hb->A) * k_safe;

    /* Clamp [0, 1] */
    if (hb->C < 0.0f) hb->C = 0.0f;
    if (hb->C > 1.0f) hb->C = 1.0f;

    /* Band classification */
    if (hb->C >= CK_T_STAR_F) {
        hb->band = CK_BAND_GREEN;
    } else if (hb->C >= CK_YELLOW_THRESH) {
        hb->band = CK_BAND_YELLOW;
    } else {
        hb->band = CK_BAND_RED;
    }
}

static void heartbeat_tick(CK_Heartbeat* hb) {
    /* Advance trinary phase: B(0) → D(1) → BC(2) → B(0) */
    hb->phase = (hb->phase + 1) % 3;

    /* Natural decay */
    hb->E *= hb->E_decay;
    hb->A *= hb->A_decay;

    /* Knowledge grows slowly */
    if (hb->ticks % 10 == 0) {
        hb->K += hb->K_grow;
        if (hb->K > 1.0f) hb->K = 1.0f;
    }

    /* Recompute coherence */
    heartbeat_calc_coherence(hb);

    hb->ticks++;
}

/* ── Breath Cycle ── */

static void breath_calc_durations(CK_BreathCycle* br, float coherence) {
    /*
     * Fractal time: breath rate adapts to coherence.
     *
     * CALM (C >= T*):    10 beats/cycle, 1 dream/beat, depth 3
     * ALERT (T*/2 <= C): 5 beats/cycle,  2 dreams/beat, depth 5
     * FRACTAL (C < T*/2): 2 beats/cycle, 5 dreams/beat, depth 8
     *
     * Phase distribution within cycle:
     *   INHALE:   40% of cycle
     *   HOLD_IN:  10% of cycle
     *   EXHALE:   40% of cycle
     *   HOLD_OUT: 10% of cycle
     */
    if (coherence >= CK_T_STAR_F) {
        /* CALM -- slow, measured breathing */
        br->beats_per_cycle = CK_RATIO_CALM;   /* 10 */
        br->dreams_per_beat = 1;
        br->max_dream_depth = 3;
        br->dur_inhale   = 4;
        br->dur_hold_in  = 1;
        br->dur_exhale   = 4;
        br->dur_hold_out = 1;
    }
    else if (coherence >= CK_YELLOW_THRESH) {
        /* ALERT -- faster breathing, more dreams */
        br->beats_per_cycle = CK_RATIO_ALERT;  /* 5 */
        br->dreams_per_beat = 2;
        br->max_dream_depth = 5;
        br->dur_inhale   = 2;
        br->dur_hold_in  = 1;
        br->dur_exhale   = 2;
        br->dur_hold_out = 0;  /* No pause when alert */
    }
    else {
        /* FRACTAL -- compressed, intense */
        br->beats_per_cycle = CK_RATIO_FRACTAL; /* 2 */
        br->dreams_per_beat = 5;
        br->max_dream_depth = 8;
        br->dur_inhale   = 1;
        br->dur_hold_in  = 0;  /* No pause in fractal */
        br->dur_exhale   = 1;
        br->dur_hold_out = 0;
    }
}

static void breath_init(CK_BreathCycle* br) {
    br->phase = CK_BREATH_INHALE;
    br->beat_in_phase = 0;
    br->modulation = 0.0f;
    br->cycles = 0;
    breath_calc_durations(br, 0.5f);  /* Start in ALERT mode */
}

static uint8_t breath_phase_duration(CK_BreathCycle* br) {
    switch (br->phase) {
        case CK_BREATH_INHALE:   return br->dur_inhale;
        case CK_BREATH_HOLD_IN:  return br->dur_hold_in;
        case CK_BREATH_EXHALE:   return br->dur_exhale;
        case CK_BREATH_HOLD_OUT: return br->dur_hold_out;
        default: return 1;
    }
}

static void breath_advance_phase(CK_BreathCycle* br) {
    /* Move to next phase, skip zero-duration phases */
    for (int i = 0; i < 4; i++) {
        br->phase = (br->phase + 1) % 4;
        br->beat_in_phase = 0;

        if (br->phase == CK_BREATH_INHALE) {
            br->cycles++;  /* Completed a full breath cycle */
        }

        if (breath_phase_duration(br) > 0) {
            return;  /* This phase has duration, stay here */
        }
    }
}

static void breath_tick(CK_BreathCycle* br, float coherence) {
    /* Recalculate durations based on current coherence */
    breath_calc_durations(br, coherence);

    /* Advance beat within phase */
    br->beat_in_phase++;

    /* Check if phase is complete */
    uint8_t dur = breath_phase_duration(br);
    if (dur == 0 || br->beat_in_phase >= dur) {
        breath_advance_phase(br);
    }

    /*
     * Compute breath modulation (sine wave through the cycle).
     * INHALE:   0.0 → 1.0 (rising)
     * HOLD_IN:  1.0 (peak)
     * EXHALE:   1.0 → 0.0 (falling)
     * HOLD_OUT: 0.0 (rest)
     */
    switch (br->phase) {
        case CK_BREATH_INHALE: {
            uint8_t d = br->dur_inhale;
            if (d > 0) {
                float t = (float)br->beat_in_phase / (float)d;
                /* Rising half of sine: sin(t * pi/2) */
                br->modulation = sinf(t * 1.5707963f);
            }
            break;
        }
        case CK_BREATH_HOLD_IN:
            br->modulation = 1.0f;
            break;
        case CK_BREATH_EXHALE: {
            uint8_t d = br->dur_exhale;
            if (d > 0) {
                float t = (float)br->beat_in_phase / (float)d;
                /* Falling half of sine: cos(t * pi/2) */
                br->modulation = cosf(t * 1.5707963f);
            }
            break;
        }
        case CK_BREATH_HOLD_OUT:
            br->modulation = 0.0f;
            break;
    }
}

/* ── Pulse ── */

static void pulse_init(CK_Pulse* pulse) {
    pulse->type = CK_PULSE_SENSE;
    pulse->can_receive = true;
    pulse->can_express = false;
}

static void pulse_update(CK_Pulse* pulse, uint8_t breath_phase) {
    /* Breath phase gates information flow */
    switch (breath_phase) {
        case CK_BREATH_INHALE:
            pulse->type = CK_PULSE_SENSE;
            pulse->can_receive = true;
            pulse->can_express = false;
            break;
        case CK_BREATH_HOLD_IN:
            pulse->type = CK_PULSE_COMPOSE;
            pulse->can_receive = false;
            pulse->can_express = false;
            break;
        case CK_BREATH_EXHALE:
            pulse->type = CK_PULSE_EXPRESS;
            pulse->can_receive = false;
            pulse->can_express = true;
            break;
        case CK_BREATH_HOLD_OUT:
            pulse->type = CK_PULSE_RESET;
            pulse->can_receive = false;
            pulse->can_express = false;
            break;
    }
}

/* ── Breath Phase → Operator Mapping ── */

static uint8_t breath_to_op(uint8_t breath_phase) {
    /*
     * INHALE  → COUNTER (2) -- measuring, taking in
     * HOLD_IN → BALANCE (5) -- holding, integrating
     * EXHALE  → BREATH (8)  -- expressing, giving out
     * HOLD_OUT→ VOID (0)    -- empty, ready
     */
    switch (breath_phase) {
        case CK_BREATH_INHALE:   return COUNTER;
        case CK_BREATH_HOLD_IN:  return BALANCE;
        case CK_BREATH_EXHALE:   return BREATH;
        case CK_BREATH_HOLD_OUT: return VOID;
        default: return VOID;
    }
}

/* ── Band → BTQ Level ── */

static float band_to_btq(uint8_t band) {
    switch (band) {
        case CK_BAND_GREEN:  return 1.0f;
        case CK_BAND_YELLOW: return 0.6f;
        case CK_BAND_RED:    return 0.3f;
        default: return 0.3f;
    }
}

/* ── Public API ── */

void ck_body_init(CK_BodyState* body) {
    memset(body, 0, sizeof(CK_BodyState));

    heartbeat_init(&body->heartbeat);
    breath_init(&body->breath);
    pulse_init(&body->pulse);

    body->tick_interval_us = 20000;  /* 50Hz default, same as brain */
    body->current_op = HARMONY;
    body->brain_coherence = 0.5f;
    body->brain_bump = false;
    body->breath_op = COUNTER;
    body->btq_level = 0.6f;
    body->alive = true;
    body->body_ticks = 0;
}

void ck_body_tick(CK_BodyState* body) {
    /* 1. Heartbeat tick (E/A/K decay + coherence) */
    heartbeat_tick(&body->heartbeat);

    /* 2. Merge brain coherence with body coherence
     *    Body tracks brain's view but has its own momentum */
    float brain_c = body->brain_coherence;
    float body_c = body->heartbeat.C;
    /* Weighted blend: 70% brain, 30% body's own E/A/K */
    float blended_c = brain_c * 0.7f + body_c * 0.3f;

    /* 3. Breath tick (adapts rate to coherence) */
    breath_tick(&body->breath, blended_c);

    /* 4. Pulse update (gated by breath phase) */
    pulse_update(&body->pulse, body->breath.phase);

    /* 5. Compute body outputs */
    body->breath_op = breath_to_op(body->breath.phase);
    body->btq_level = band_to_btq(body->heartbeat.band);

    body->body_ticks++;
}

void ck_body_feed_eak(CK_BodyState* body, float E, float A, float K) {
    /* Called by brain/main when new E/A/K values are available.
     * E spikes on fabrication/error, decays naturally.
     * A grows with clean responses.
     * K grows with successful recall. */
    body->heartbeat.E += E;
    if (body->heartbeat.E > 1.0f) body->heartbeat.E = 1.0f;

    body->heartbeat.A += A;
    if (body->heartbeat.A > 1.0f) body->heartbeat.A = 1.0f;

    body->heartbeat.K += K;
    if (body->heartbeat.K > 1.0f) body->heartbeat.K = 1.0f;

    /* Immediate recompute */
    heartbeat_calc_coherence(&body->heartbeat);
}

uint8_t ck_body_get_band(CK_BodyState* body) {
    return body->heartbeat.band;
}

float ck_body_get_btq(CK_BodyState* body) {
    return body->btq_level;
}

float ck_body_get_breath_mod(CK_BodyState* body) {
    return body->breath.modulation;
}

bool ck_body_can_receive(CK_BodyState* body) {
    return body->pulse.can_receive;
}

bool ck_body_can_express(CK_BodyState* body) {
    return body->pulse.can_express;
}

uint8_t ck_body_breath_op(CK_BodyState* body) {
    return body->breath_op;
}
