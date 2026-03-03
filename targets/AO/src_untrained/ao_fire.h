/*
 * ao_fire.h -- D3 / Binding / Jerk / Engine
 *
 * The heartbeat, the brain, the body, the decision kernel.
 * Everything that RUNS. Fire is intensity.
 */
/*
 * Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
 * Licensed under the 7Site Human Use License v1.0
 * See LICENSE file in project root for full terms.
 *
 * FREE for humans for personal/recreational use.
 * NO commercial or government use without written agreement.
 */


#ifndef AO_FIRE_H
#define AO_FIRE_H

#include "ao_earth.h"

/* ── Heartbeat ── */
typedef struct {
    int running_fuse;
    int tick_count;
    float energy;
    int bumps_hit;
    float total_mass_spent;
} AO_Heartbeat;

typedef struct {
    int result;
    int bump;
    float mass_cost;
    float energy;
    int running_fuse;
    int tick;
} AO_HeartbeatResult;

void ao_hb_init(AO_Heartbeat* h);
void ao_hb_tick(AO_Heartbeat* h, int phase_b, int phase_d, int shell,
                AO_HeartbeatResult* out);
void ao_hb_reset_energy(AO_Heartbeat* h);

/* ── Brain (transition lattice) ── */
typedef struct {
    uint32_t tl[AO_NUM_OPS][AO_NUM_OPS];
    uint32_t total;
    int last_op; /* -1 = none */
} AO_Brain;

void  ao_brain_init(AO_Brain* b);
void  ao_brain_observe(AO_Brain* b, int op);
int   ao_brain_predict(const AO_Brain* b, int current_op);
void  ao_brain_predict_weighted(const AO_Brain* b, int current_op,
                                float out[AO_NUM_OPS]);
float ao_brain_entropy(const AO_Brain* b);
void  ao_brain_top_transitions(const AO_Brain* b, int* from_ops, int* to_ops,
                               int* counts, int max_n, int* out_n);
void  ao_brain_reset(AO_Brain* b);

/* ── Body (E/A/K + breath + wobble) ── */
typedef struct {
    float E, A, K;          /* Error, Alert, Knowing */
    int breath_phase;       /* 0=inhale, 1=hold, 2=exhale, 3=hold */
    int breath_counter;
    int breath_rate;        /* ticks per phase: GREEN=10, YELLOW=5, RED=2 */
    int wobble_index;       /* 0=becoming, 1=being, 2=doing */
    int wobble_counter;
    int tick_count;
} AO_Body;

void  ao_body_init(AO_Body* b);
void  ao_body_tick(AO_Body* b, float coherence, int bump, float novelty);
float ao_body_coherence(const AO_Body* b);
int   ao_body_band(const AO_Body* b);
int   ao_body_is_exhaling(const AO_Body* b);
float ao_body_wobble_value(const AO_Body* b);

/* ── BTQ Decision Kernel ── */
typedef struct {
    int last_decision;
    int decision_count;
} AO_BTQ;

void ao_btq_init(AO_BTQ* q);
int  ao_btq_decide(AO_BTQ* q, int current_op, const AO_Brain* brain,
                   float coherence, float body_coherence, int shell);

#endif /* AO_FIRE_H */
