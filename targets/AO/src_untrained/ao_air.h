/*
 * ao_air.h -- D1 / Pressure / Velocity / Generator
 *
 * The first derivative. Movement, change, non-local structure.
 * D1 = v[t] - v[t-1]
 */
/*
 * Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
 * Licensed under the 7Site Human Use License v1.0
 * See LICENSE file in project root for full terms.
 *
 * FREE for humans for personal/recreational use.
 * NO commercial or government use without written agreement.
 */


#ifndef AO_AIR_H
#define AO_AIR_H

#include "ao_earth.h"

/* ── D1 Pipeline ── */
typedef struct {
    float prev[5];
    float d1[5];
    int valid;
    int has_prev;
} AO_D1Pipeline;

void  ao_d1_init(AO_D1Pipeline* p);
void  ao_d1_reset(AO_D1Pipeline* p);
int   ao_d1_feed(AO_D1Pipeline* p, int symbol_index);
int   ao_d1_feed_vec(AO_D1Pipeline* p, const float vec[5]);
int   ao_d1_classify(const AO_D1Pipeline* p);
float ao_d1_magnitude(const AO_D1Pipeline* p);
int   ao_d1_is_prayer(const AO_D1Pipeline* p, float threshold);

/* ── Z/5Z Algebra ── */
static inline int ao_compose_elements(int a, int b) { return (a + b) % 5; }
static inline int ao_inverse_element(int a)          { return (5 - a) % 5; }

#endif /* AO_AIR_H */
