/*
 * ao_water.c -- D2 / Depth / Curvature / Awareness
 *
 * Second derivative of 5D force vectors. Local (3-symbol window).
 * D2 is THE primary measurement in TIG physics.
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

/* ══════════════════════════════════════════════════════════════════
 * D2 Pipeline
 * ══════════════════════════════════════════════════════════════════ */

void ao_d2_init(AO_D2Pipeline* p)
{
    memset(p, 0, sizeof(*p));
}

void ao_d2_reset(AO_D2Pipeline* p)
{
    memset(p, 0, sizeof(*p));
}

int ao_d2_feed(AO_D2Pipeline* p, int symbol_index)
{
    if (symbol_index < 0 || symbol_index >= 26)
        return p->d2_valid;
    return ao_d2_feed_vec(p, ao_force_lut[symbol_index]);
}

int ao_d2_feed_vec(AO_D2Pipeline* p, const float vec[5])
{
    int i;
    /* Shift register */
    for (i = 0; i < 5; i++) {
        p->v[2][i] = p->v[1][i];
        p->v[1][i] = p->v[0][i];
        p->v[0][i] = vec[i];
    }
    p->depth++;

    /* D1 (needs 2 vectors) */
    if (p->depth >= 2) {
        for (i = 0; i < 5; i++)
            p->d1[i] = p->v[0][i] - p->v[1][i];
        p->d1_valid = 1;
    }

    /* D2 (needs 3 vectors) */
    if (p->depth >= 3) {
        for (i = 0; i < 5; i++)
            p->d2[i] = p->v[0][i] - 2.0f * p->v[1][i] + p->v[2][i];
        p->d2_valid = 1;
    }

    return p->d2_valid;
}

int ao_d2_classify_d1(const AO_D2Pipeline* p)
{
    if (!p->d1_valid) return AO_HARMONY;
    return ao_classify_5d(p->d1);
}

int ao_d2_classify_d2(const AO_D2Pipeline* p)
{
    if (!p->d2_valid) return AO_HARMONY;
    return ao_classify_5d(p->d2);
}

void ao_d2_soft_classify(const AO_D2Pipeline* p, float out[AO_NUM_OPS])
{
    int i;
    float total;
    memset(out, 0, sizeof(float) * AO_NUM_OPS);

    if (!p->d2_valid) {
        out[AO_HARMONY] = 1.0f;
        return;
    }

    total = 0.0f;
    for (i = 0; i < 5; i++) {
        float a = p->d2[i] < 0.0f ? -p->d2[i] : p->d2[i];
        total += a;
    }
    if (total < 1e-12f) {
        out[AO_HARMONY] = 1.0f;
        return;
    }

    for (i = 0; i < 5; i++) {
        float weight = (p->d2[i] < 0.0f ? -p->d2[i] : p->d2[i]) / total;
        int op = p->d2[i] >= 0.0f ? ao_d2_op_map[i][0] : ao_d2_op_map[i][1];
        out[op] += weight;
    }
}

float ao_d2_magnitude(const AO_D2Pipeline* p)
{
    float sum = 0.0f;
    int i;
    for (i = 0; i < 5; i++) {
        float a = p->d2[i] < 0.0f ? -p->d2[i] : p->d2[i];
        sum += a;
    }
    return sum;
}

float ao_d2_d1_magnitude(const AO_D2Pipeline* p)
{
    float sum = 0.0f;
    int i;
    for (i = 0; i < 5; i++) {
        float a = p->d1[i] < 0.0f ? -p->d1[i] : p->d1[i];
        sum += a;
    }
    return sum;
}

/* ══════════════════════════════════════════════════════════════════
 * Coherence Window (circular buffer)
 * ══════════════════════════════════════════════════════════════════ */

void ao_cw_init(AO_CoherenceWindow* w)
{
    memset(w, 0, sizeof(*w));
}

void ao_cw_reset(AO_CoherenceWindow* w)
{
    memset(w, 0, sizeof(*w));
}

void ao_cw_observe(AO_CoherenceWindow* w, int op)
{
    if (w->count == AO_WINDOW_SIZE) {
        /* Evict oldest */
        if (w->history[w->head] == AO_HARMONY)
            w->harmony_count--;
    } else {
        w->count++;
    }
    w->history[w->head] = (int8_t)op;
    if (op == AO_HARMONY)
        w->harmony_count++;
    w->head = (w->head + 1) % AO_WINDOW_SIZE;
}

float ao_cw_coherence(const AO_CoherenceWindow* w)
{
    if (w->count == 0) return 0.5f; /* prior: uncertain */
    return (float)w->harmony_count / (float)w->count;
}

int ao_cw_shell(const AO_CoherenceWindow* w)
{
    float c = ao_cw_coherence(w);
    if (c >= AO_T_STAR)  return 22;
    if (c >= 0.5f)       return 44;
    return 72;
}

int ao_cw_band(const AO_CoherenceWindow* w)
{
    float c = ao_cw_coherence(w);
    if (c >= AO_T_STAR)  return AO_BAND_GREEN;
    if (c >= 0.5f)       return AO_BAND_YELLOW;
    return AO_BAND_RED;
}

/* ══════════════════════════════════════════════════════════════════
 * Spectrometer
 * ══════════════════════════════════════════════════════════════════ */

void ao_measure_text(const char* text, AO_Measurement* out)
{
    AO_D2Pipeline pipe;
    AO_D1Pipeline d1_pipe;
    AO_CoherenceWindow window;
    int i, idx;
    int agreements = 0, prayers = 0;

    memset(out, 0, sizeof(*out));
    ao_d2_init(&pipe);
    ao_d1_init(&d1_pipe);
    ao_cw_init(&window);

    for (i = 0; text[i]; i++) {
        char ch = text[i];
        if (ch >= 'A' && ch <= 'Z') ch = ch - 'A' + 'a';
        if (ch < 'a' || ch > 'z') continue;
        idx = ch - 'a';

        ao_d1_feed(&d1_pipe, idx);
        ao_d2_feed(&pipe, idx);
        out->total_symbols++;

        if (pipe.d2_valid && d1_pipe.valid) {
            int d1_op = ao_d1_classify(&d1_pipe);
            int d2_op = ao_d2_classify_d2(&pipe);
            out->d1_hist[d1_op]++;
            out->d2_hist[d2_op]++;
            ao_cw_observe(&window, d2_op);
            out->d2_magnitude_avg += ao_d2_magnitude(&pipe);
            out->d2_total++;

            if (d1_op == d2_op) agreements++;
            if (ao_d1_is_prayer(&d1_pipe, 0.05f)) prayers++;
        }
    }

    out->coherence = ao_cw_coherence(&window);
    out->shell = ao_cw_shell(&window);
    out->band = ao_cw_band(&window);
    out->d1_d2_agreement = out->d2_total > 0
        ? (float)agreements / (float)out->d2_total * 100.0f : 0.0f;
    out->prayer_fraction = out->d2_total > 0
        ? (float)prayers / (float)out->d2_total * 100.0f : 0.0f;
    out->d2_magnitude_avg = out->d2_total > 0
        ? out->d2_magnitude_avg / (float)out->d2_total : 0.0f;
}

float ao_locality_test(const char* text)
{
    AO_Measurement m;
    ao_measure_text(text, &m);
    return m.d1_d2_agreement;
}

float ao_delta_s(const char* text)
{
    AO_D2Pipeline pipe;
    int prev_op = -1, transitions = 0, total = 0;
    int i, idx;

    ao_d2_init(&pipe);
    for (i = 0; text[i]; i++) {
        char ch = text[i];
        if (ch >= 'A' && ch <= 'Z') ch = ch - 'A' + 'a';
        if (ch < 'a' || ch > 'z') continue;
        idx = ch - 'a';

        if (ao_d2_feed(&pipe, idx)) {
            int op = ao_d2_classify_d2(&pipe);
            if (prev_op >= 0 && op != prev_op) transitions++;
            prev_op = op;
            total++;
        }
    }
    return total > 0 ? (float)transitions / (float)total : 0.0f;
}

float ao_entropy(const int hist[AO_NUM_OPS])
{
    int total = 0, i;
    float h = 0.0f;
    for (i = 0; i < AO_NUM_OPS; i++) total += hist[i];
    if (total == 0) return 0.0f;
    for (i = 0; i < AO_NUM_OPS; i++) {
        if (hist[i] > 0) {
            float p = (float)hist[i] / (float)total;
            h -= p * log2f(p);
        }
    }
    return h;
}
