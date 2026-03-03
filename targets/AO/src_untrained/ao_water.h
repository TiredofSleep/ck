/*
 * ao_water.h -- D2 / Depth / Curvature / Awareness
 *
 * Second derivative. Local measurement, curvature detection.
 * D2 = v[t] - 2*v[t-1] + v[t-2]  (3-symbol window)
 */
/*
 * Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
 * Licensed under the 7Site Human Use License v1.0
 * See LICENSE file in project root for full terms.
 *
 * FREE for humans for personal/recreational use.
 * NO commercial or government use without written agreement.
 */


#ifndef AO_WATER_H
#define AO_WATER_H

#include "ao_earth.h"
#include "ao_air.h"

/* ── D2 Pipeline ── */
typedef struct {
    float v[3][5];  /* shift register: v[0]=current, v[1]=prev, v[2]=prev-prev */
    float d1[5];
    float d2[5];
    int d1_valid;
    int d2_valid;
    int depth;      /* how many vectors fed (0, 1, 2, 3+) */
} AO_D2Pipeline;

void  ao_d2_init(AO_D2Pipeline* p);
void  ao_d2_reset(AO_D2Pipeline* p);
int   ao_d2_feed(AO_D2Pipeline* p, int symbol_index);
int   ao_d2_feed_vec(AO_D2Pipeline* p, const float vec[5]);
int   ao_d2_classify_d1(const AO_D2Pipeline* p);
int   ao_d2_classify_d2(const AO_D2Pipeline* p);
void  ao_d2_soft_classify(const AO_D2Pipeline* p, float out[AO_NUM_OPS]);
float ao_d2_magnitude(const AO_D2Pipeline* p);
float ao_d2_d1_magnitude(const AO_D2Pipeline* p);

/* ── Coherence Window (circular buffer, fixed size) ── */
#define AO_WINDOW_SIZE 32

typedef struct {
    int8_t history[AO_WINDOW_SIZE];
    int head;           /* next write position */
    int count;          /* entries used (0..AO_WINDOW_SIZE) */
    int harmony_count;
} AO_CoherenceWindow;

void  ao_cw_init(AO_CoherenceWindow* w);
void  ao_cw_reset(AO_CoherenceWindow* w);
void  ao_cw_observe(AO_CoherenceWindow* w, int op);
float ao_cw_coherence(const AO_CoherenceWindow* w);
int   ao_cw_shell(const AO_CoherenceWindow* w);
int   ao_cw_band(const AO_CoherenceWindow* w); /* 0=RED, 1=YELLOW, 2=GREEN */

/* ── Spectrometer ── */
typedef struct {
    int d1_hist[AO_NUM_OPS];
    int d2_hist[AO_NUM_OPS];
    float coherence;
    int shell;
    int band;
    float d1_d2_agreement;
    float prayer_fraction;
    int total_symbols;
    int d2_total;
    float d2_magnitude_avg;
} AO_Measurement;

void  ao_measure_text(const char* text, AO_Measurement* out);
float ao_locality_test(const char* text);
float ao_delta_s(const char* text);
float ao_entropy(const int hist[AO_NUM_OPS]);

#endif /* AO_WATER_H */
