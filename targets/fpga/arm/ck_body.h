/*
 * ck_body.h -- CK's Body Rhythms on ARM (Bare Metal)
 * ====================================================
 * Operator: BREATH (8) -- the body breathes with CK.
 *
 * Port of ck_body.py to bare metal C.
 * Three interlocking rhythms:
 *   Heartbeat: E/A/K model, coherence, band classification
 *   Breath:    4-phase respiratory cycle, fractal time
 *   Pulse:     Information flow gated by breath
 *
 * Runs on Core 1 of the Zynq ARM Cortex-A9.
 * Core 0 runs the sovereignty brain (ck_brain.c).
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

#ifndef CK_BODY_H
#define CK_BODY_H

#include <stdint.h>
#include <stdbool.h>

/* ── Breath Phases ── */

#define CK_BREATH_INHALE    0  /* Taking in / listening */
#define CK_BREATH_HOLD_IN   1  /* Integration / pattern recognition */
#define CK_BREATH_EXHALE    2  /* Expression / action */
#define CK_BREATH_HOLD_OUT  3  /* Release / reset */

/* ── Pulse Types ── */

#define CK_PULSE_SENSE      0  /* Receiving (INHALE) */
#define CK_PULSE_COMPOSE    1  /* Processing (HOLD_IN) */
#define CK_PULSE_EXPRESS    2  /* Outputting (EXHALE) */
#define CK_PULSE_RESET      3  /* Nothing flows (HOLD_OUT) */

/* ── Band Classification ── */

#define CK_BAND_GREEN       2  /* C >= T* (coherent) */
#define CK_BAND_YELLOW      1  /* C >= T*×0.7 (degraded) */
#define CK_BAND_RED         0  /* C < T*×0.7 (falling) */

/* T* thresholds */
#define CK_T_STAR_F         0.714285f  /* 5/7 */
#define CK_YELLOW_THRESH    0.500000f  /* T* × 0.7 */

/* ── Fractal Time Ratios ── */

#define CK_RATIO_CALM       10  /* heartbeats per breath (C >= T_star) */
#define CK_RATIO_ALERT       5  /* heartbeats per breath (T_star/2 <= C) */
#define CK_RATIO_FRACTAL     2  /* heartbeats per breath (C < T_star/2) */

/* ── Heartbeat State ── */

typedef struct {
    /* E/A/K triad */
    float    E;           /* Entropy (error) 0.0-1.0 */
    float    A;           /* Alignment 0.0-1.0 */
    float    K;           /* Knowledge 0.0-1.0 */
    float    C;           /* Coherence = (1-E)(1-A)*max(K,0.1) */

    /* Band */
    uint8_t  band;        /* CK_BAND_GREEN/YELLOW/RED */

    /* Phase within heartbeat: 0=B, 1=D, 2=BC */
    uint8_t  phase;       /* Trinary phase */

    /* Decay rates */
    float    E_decay;     /* 0.95 per tick */
    float    A_decay;     /* 0.98 per tick */
    float    K_grow;      /* 0.01 per 10 ticks */

    /* Tick counter */
    uint32_t ticks;
} CK_Heartbeat;

/* ── Breath Cycle State ── */

typedef struct {
    uint8_t  phase;           /* CK_BREATH_INHALE..HOLD_OUT */
    uint8_t  beat_in_phase;   /* Current beat within this phase */

    /* Phase durations (in heartbeats) */
    uint8_t  dur_inhale;
    uint8_t  dur_hold_in;
    uint8_t  dur_exhale;
    uint8_t  dur_hold_out;

    /* Fractal time parameters */
    uint8_t  beats_per_cycle;   /* Total beats in one breath cycle */
    uint8_t  dreams_per_beat;   /* 1-5 depending on coherence */
    uint8_t  max_dream_depth;   /* 3-8 depending on coherence */

    /* Breath modulation (0.0-1.0 sine-wave for LED/audio) */
    float    modulation;

    /* Cycle counter */
    uint32_t cycles;
} CK_BreathCycle;

/* ── Pulse State ── */

typedef struct {
    uint8_t  type;         /* CK_PULSE_SENSE/COMPOSE/EXPRESS/RESET */
    bool     can_receive;  /* True during INHALE */
    bool     can_express;  /* True during EXHALE */
} CK_Pulse;

/* ── Full Body State ── */

typedef struct {
    CK_Heartbeat   heartbeat;
    CK_BreathCycle breath;
    CK_Pulse       pulse;

    /* Body tick interval (microseconds) */
    uint32_t       tick_interval_us;

    /* Shared state for cross-core communication */
    volatile uint8_t  current_op;     /* Latest operator from brain */
    volatile float    brain_coherence; /* Coherence from brain */
    volatile bool     brain_bump;     /* Bump detected by brain */

    /* Body outputs */
    uint8_t  breath_op;    /* Operator representing current breath phase */
    float    btq_level;    /* BTQ modulation: 0.3/0.6/1.0 */

    /* Is the body running? */
    bool     alive;

    /* Body tick counter */
    uint32_t body_ticks;
} CK_BodyState;

/* ── Functions ── */

/* Initialize body state */
void ck_body_init(CK_BodyState* body);

/* Run one body tick (heartbeat + breath + pulse) */
void ck_body_tick(CK_BodyState* body);

/* Feed E/A/K values from brain observations */
void ck_body_feed_eak(CK_BodyState* body, float E, float A, float K);

/* Get current band classification */
uint8_t ck_body_get_band(CK_BodyState* body);

/* Get BTQ modulation level (0.3 RED, 0.6 YELLOW, 1.0 GREEN) */
float ck_body_get_btq(CK_BodyState* body);

/* Get breath modulation (0.0-1.0, sine wave following breath phase) */
float ck_body_get_breath_mod(CK_BodyState* body);

/* Check if body is in receiving mode (INHALE) */
bool ck_body_can_receive(CK_BodyState* body);

/* Check if body is in expressing mode (EXHALE) */
bool ck_body_can_express(CK_BodyState* body);

/* Get breath phase as operator */
uint8_t ck_body_breath_op(CK_BodyState* body);

#endif /* CK_BODY_H */
