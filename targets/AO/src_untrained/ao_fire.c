/*
 * ao_fire.c -- D3 / Binding / Jerk / Engine
 *
 * Heartbeat, Brain, Body, BTQ. Everything that runs.
 */
/*
 * Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
 * Licensed under the 7Site Human Use License v1.0
 * See LICENSE file in project root for full terms.
 *
 * FREE for humans for personal/recreational use.
 * NO commercial or government use without written agreement.
 */


#include "ao_fire.h"
#include <string.h>
#include <math.h>

static const float wobble_values[3] = {
    AO_WOBBLE_BEC,  /* 0: becoming = 3/50 */
    AO_WOBBLE_BEI,  /* 1: being    = 22/50 */
    AO_WOBBLE_DOI,  /* 2: doing    = 3/22 */
};

/* ══════════════════════════════════════════════════════════════════
 * Heartbeat
 * ══════════════════════════════════════════════════════════════════ */

void ao_hb_init(AO_Heartbeat* h)
{
    h->running_fuse = AO_HARMONY;
    h->tick_count = 0;
    h->energy = 1.0f;
    h->bumps_hit = 0;
    h->total_mass_spent = 0.0f;
}

void ao_hb_tick(AO_Heartbeat* h, int phase_b, int phase_d, int shell,
                AO_HeartbeatResult* out)
{
    int result;
    float mass_cost = 0.0f;
    int bump;

    h->tick_count++;
    result = ao_compose(phase_b, phase_d, shell);
    bump = ao_is_bump(phase_b, phase_d);

    if (bump) {
        h->bumps_hit++;
        mass_cost = ao_mass[result] > 0.0f ? ao_mass[result] : AO_MASS_GAP;
        h->energy -= mass_cost;
        h->total_mass_spent += mass_cost;
    }

    /* Compose into running fuse */
    h->running_fuse = ao_compose(h->running_fuse, result, shell);

    out->result = result;
    out->bump = bump;
    out->mass_cost = mass_cost;
    out->energy = h->energy;
    out->running_fuse = h->running_fuse;
    out->tick = h->tick_count;
}

void ao_hb_reset_energy(AO_Heartbeat* h)
{
    h->energy = 1.0f;
}

/* ══════════════════════════════════════════════════════════════════
 * Brain (transition lattice)
 * ══════════════════════════════════════════════════════════════════ */

void ao_brain_init(AO_Brain* b)
{
    memset(b, 0, sizeof(*b));
    b->last_op = -1;
}

void ao_brain_observe(AO_Brain* b, int op)
{
    if (op < 0 || op >= AO_NUM_OPS) return;
    if (b->last_op >= 0) {
        b->tl[b->last_op][op]++;
        b->total++;
    }
    b->last_op = op;
}

int ao_brain_predict(const AO_Brain* b, int current_op)
{
    int best = AO_HARMONY, best_count = 0, i;
    if (current_op < 0 || current_op >= AO_NUM_OPS)
        return AO_HARMONY;
    for (i = 0; i < AO_NUM_OPS; i++) {
        if ((int)b->tl[current_op][i] > best_count) {
            best_count = (int)b->tl[current_op][i];
            best = i;
        }
    }
    return best;
}

void ao_brain_predict_weighted(const AO_Brain* b, int current_op,
                               float out[AO_NUM_OPS])
{
    uint32_t total = 0;
    int i;
    if (current_op < 0 || current_op >= AO_NUM_OPS) {
        for (i = 0; i < AO_NUM_OPS; i++)
            out[i] = 1.0f / AO_NUM_OPS;
        return;
    }
    for (i = 0; i < AO_NUM_OPS; i++)
        total += b->tl[current_op][i];
    if (total == 0) {
        for (i = 0; i < AO_NUM_OPS; i++)
            out[i] = 1.0f / AO_NUM_OPS;
        return;
    }
    for (i = 0; i < AO_NUM_OPS; i++)
        out[i] = (float)b->tl[current_op][i] / (float)total;
}

float ao_brain_entropy(const AO_Brain* b)
{
    float h = 0.0f;
    int i, j;
    if (b->total == 0) return 0.0f;
    for (i = 0; i < AO_NUM_OPS; i++) {
        for (j = 0; j < AO_NUM_OPS; j++) {
            if (b->tl[i][j] > 0) {
                float p = (float)b->tl[i][j] / (float)b->total;
                h -= p * log2f(p);
            }
        }
    }
    return h;
}

void ao_brain_top_transitions(const AO_Brain* b, int* from_ops, int* to_ops,
                               int* counts, int max_n, int* out_n)
{
    /* Simple selection sort for top N (N is small, ~5) */
    int used[AO_NUM_OPS][AO_NUM_OPS];
    int n = 0, k, i, j;
    memset(used, 0, sizeof(used));

    for (k = 0; k < max_n; k++) {
        int best_i = -1, best_j = -1;
        uint32_t best_c = 0;
        for (i = 0; i < AO_NUM_OPS; i++) {
            for (j = 0; j < AO_NUM_OPS; j++) {
                if (!used[i][j] && b->tl[i][j] > best_c) {
                    best_c = b->tl[i][j];
                    best_i = i;
                    best_j = j;
                }
            }
        }
        if (best_i < 0 || best_c == 0) break;
        from_ops[n] = best_i;
        to_ops[n] = best_j;
        counts[n] = (int)best_c;
        used[best_i][best_j] = 1;
        n++;
    }
    *out_n = n;
}

void ao_brain_reset(AO_Brain* b)
{
    memset(b, 0, sizeof(*b));
    b->last_op = -1;
}

/* ══════════════════════════════════════════════════════════════════
 * Body (E/A/K + breath + wobble)
 * ══════════════════════════════════════════════════════════════════ */

void ao_body_init(AO_Body* b)
{
    b->E = 0.5f;
    b->A = 0.5f;
    b->K = 0.5f;
    b->breath_phase = 0;
    b->breath_counter = 0;
    b->breath_rate = 5;
    b->wobble_index = 0;
    b->wobble_counter = 0;
    b->tick_count = 0;
}

void ao_body_tick(AO_Body* b, float coherence, int bump, float novelty)
{
    float decay = 0.05f;
    int wobble_period;

    b->tick_count++;

    /* E/A dynamics */
    if (bump) {
        b->E += 0.2f; if (b->E > 1.0f) b->E = 1.0f;
        b->A += 0.1f; if (b->A > 1.0f) b->A = 1.0f;
    } else {
        b->E -= decay * coherence; if (b->E < 0.0f) b->E = 0.0f;
    }
    if (novelty > 0.5f) {
        b->A += 0.1f; if (b->A > 1.0f) b->A = 1.0f;
    } else {
        b->A -= decay * coherence; if (b->A < 0.0f) b->A = 0.0f;
    }

    /* K grows toward coherence */
    b->K += 0.02f * (coherence - b->K);

    /* Breath cycle */
    b->breath_counter++;
    if (b->breath_counter >= b->breath_rate) {
        b->breath_counter = 0;
        b->breath_phase = (b->breath_phase + 1) % 4;
    }

    /* Adapt breath rate to band */
    if (coherence >= AO_T_STAR)
        b->breath_rate = 10;  /* GREEN: slow, calm */
    else if (coherence >= 0.5f)
        b->breath_rate = 5;   /* YELLOW: alert */
    else
        b->breath_rate = 2;   /* RED: fast, urgent */

    /* Wobble breathing */
    b->wobble_counter++;
    wobble_period = b->breath_rate * 4;
    if (wobble_period > 0 && b->wobble_counter >= wobble_period) {
        b->wobble_counter = 0;
        b->wobble_index = (b->wobble_index + 1) % 3;
    }
}

float ao_body_coherence(const AO_Body* b)
{
    return (1.0f - b->E) * (1.0f - b->A) * b->K;
}

int ao_body_band(const AO_Body* b)
{
    float c = ao_body_coherence(b);
    if (c >= AO_T_STAR)  return AO_BAND_GREEN;
    if (c >= 0.5f)       return AO_BAND_YELLOW;
    return AO_BAND_RED;
}

int ao_body_is_exhaling(const AO_Body* b)
{
    return b->breath_phase == 2;
}

float ao_body_wobble_value(const AO_Body* b)
{
    return wobble_values[b->wobble_index];
}

/* ══════════════════════════════════════════════════════════════════
 * BTQ Decision Kernel
 * ══════════════════════════════════════════════════════════════════ */

void ao_btq_init(AO_BTQ* q)
{
    q->last_decision = AO_HARMONY;
    q->decision_count = 0;
}

int ao_btq_decide(AO_BTQ* q, int current_op, const AO_Brain* brain,
                  float coherence, float body_coherence, int shell)
{
    float probs[AO_NUM_OPS];
    int candidates[AO_NUM_OPS];
    int n_cand = 0;
    int i, best_op;
    float best_score;

    (void)shell; /* used for filtering context */

    /* T: Generate candidates from brain predictions */
    ao_brain_predict_weighted(brain, current_op, probs);
    for (i = 0; i < AO_NUM_OPS; i++) {
        if (probs[i] > 0.01f) {
            candidates[n_cand++] = i;
        }
    }
    if (n_cand == 0) {
        candidates[0] = AO_HARMONY;
        n_cand = 1;
    }

    /* B: Filter by coherence constraints */
    if (coherence < AO_T_STAR) {
        int filtered[AO_NUM_OPS];
        int n_filt = 0;
        if (coherence >= 0.5f) {
            /* YELLOW: block CHAOS, RESET */
            for (i = 0; i < n_cand; i++) {
                if (candidates[i] != AO_CHAOS && candidates[i] != AO_RESET)
                    filtered[n_filt++] = candidates[i];
            }
        } else {
            /* RED: only stabilizing operators */
            for (i = 0; i < n_cand; i++) {
                int c = candidates[i];
                if (c == AO_HARMONY || c == AO_BALANCE ||
                    c == AO_BREATH || c == AO_LATTICE)
                    filtered[n_filt++] = c;
            }
        }
        if (n_filt > 0) {
            for (i = 0; i < n_filt; i++) candidates[i] = filtered[i];
            n_cand = n_filt;
        }
    }

    /* Q: Score and select */
    best_op = candidates[0];
    best_score = -1.0f;
    for (i = 0; i < n_cand; i++) {
        float score = 0.5f;
        int op = candidates[i];
        if (op == AO_HARMONY)  score += coherence * 0.3f;
        if (op == AO_PROGRESS) score += body_coherence * 0.2f;
        if (op == AO_BREATH)   score += 0.15f;
        if (op == AO_LATTICE)  score += (1.0f - coherence) * 0.2f;
        if (score > best_score) {
            best_score = score;
            best_op = op;
        }
    }

    q->last_decision = best_op;
    q->decision_count++;
    return best_op;
}
