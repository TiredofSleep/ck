/*
 * ao_air.c -- D1 / Pressure / Velocity / Generator
 *
 * First derivative of 5D force vectors. Non-local.
 */
/*
 * Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
 * Licensed under the 7Site Human Use License v1.0
 * See LICENSE file in project root for full terms.
 *
 * FREE for humans for personal/recreational use.
 * NO commercial or government use without written agreement.
 */


#include "ao_air.h"
#include <string.h>

void ao_d1_init(AO_D1Pipeline* p)
{
    memset(p, 0, sizeof(*p));
}

void ao_d1_reset(AO_D1Pipeline* p)
{
    memset(p, 0, sizeof(*p));
}

int ao_d1_feed(AO_D1Pipeline* p, int symbol_index)
{
    if (symbol_index < 0 || symbol_index >= 26)
        return p->valid;
    return ao_d1_feed_vec(p, ao_force_lut[symbol_index]);
}

int ao_d1_feed_vec(AO_D1Pipeline* p, const float vec[5])
{
    int i;
    if (p->has_prev) {
        for (i = 0; i < 5; i++)
            p->d1[i] = vec[i] - p->prev[i];
        p->valid = 1;
    }
    for (i = 0; i < 5; i++)
        p->prev[i] = vec[i];
    p->has_prev = 1;
    return p->valid;
}

int ao_d1_classify(const AO_D1Pipeline* p)
{
    if (!p->valid)
        return AO_HARMONY;
    return ao_classify_5d(p->d1);
}

float ao_d1_magnitude(const AO_D1Pipeline* p)
{
    float sum = 0.0f;
    int i;
    for (i = 0; i < 5; i++) {
        float a = p->d1[i] < 0.0f ? -p->d1[i] : p->d1[i];
        sum += a;
    }
    return sum;
}

int ao_d1_is_prayer(const AO_D1Pipeline* p, float threshold)
{
    return p->valid && ao_d1_magnitude(p) < threshold;
}
