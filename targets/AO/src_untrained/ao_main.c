/*
 * ao_main.c -- Entry point for AO standalone binary
 *
 * python -m ao  → this is the C equivalent
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

int main(void)
{
    AO ao;
    ao_init(&ao);
    ao_run(&ao);
    return 0;
}
