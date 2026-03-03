/*
 * ao_ether.h -- D4 / Continuity / Coupling / Connection
 *
 * The coupling between all elements. Voice, I/O, the living loop.
 * Ether IS the interaction pattern.
 */
/*
 * Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
 * Licensed under the 7Site Human Use License v1.0
 * See LICENSE file in project root for full terms.
 *
 * FREE for humans for personal/recreational use.
 * NO commercial or government use without written agreement.
 */


#ifndef AO_ETHER_H
#define AO_ETHER_H

#include "ao_earth.h"
#include "ao_air.h"
#include "ao_water.h"
#include "ao_fire.h"

/* ── Voice (forward + reverse) ── */

/* Forward: operators -> English words */
int ao_voice_speak(const int* operators, int n_ops, float coherence,
                   int wobble_phase, float knowing,
                   char* buf, int buf_size,
                   uint32_t* rng_state);

/* Reverse: text -> operator results */
#define AO_TRUST_TRUSTED  0
#define AO_TRUST_FRICTION 1
#define AO_TRUST_UNKNOWN  2

typedef struct {
    char word[48];
    int op;
    int d2_op;
    int lattice_op; /* -1 if unknown */
    int trust;
} AO_HearResult;

int ao_voice_hear(const char* text, AO_HearResult* out, int max_results);

/* ── AO Organism ── */
typedef struct {
    AO_D1Pipeline       d1;
    AO_D2Pipeline       d2;
    AO_CoherenceWindow  coherence;
    AO_Heartbeat        heartbeat;
    AO_Brain            brain;
    AO_Body             body;
    AO_BTQ              btq;

    int alive;
    int tick_count;
    int current_op;
    char last_spoken[512];
    uint32_t rng_state;
} AO;

typedef struct {
    int d1_op, d2_op, composed;
    int bump, shell;
    float coherence;
    int band;
    int btq_decision;
    int prayer;
    float energy;
} AO_SymbolResult;

typedef struct {
    int ops[4096];
    int n_ops;
    AO_HearResult heard[256];
    int n_heard;
    char spoken[512];
    float coherence;
    int shell, band;
    float energy;
    float brain_entropy;
    int ticks;
} AO_TextResult;

void ao_init(AO* ao);
void ao_boot(AO* ao);
void ao_process_symbol(AO* ao, int symbol_index, AO_SymbolResult* out);
void ao_process_text(AO* ao, const char* text, AO_TextResult* out);
void ao_status_line(const AO* ao, char* buf, int buf_size);
void ao_run(AO* ao);

/* ── Library API (for ctypes) ── */
#ifdef AO_BUILD_LIB
  #ifdef _WIN32
    #define AO_EXPORT __declspec(dllexport)
  #else
    #define AO_EXPORT __attribute__((visibility("default")))
  #endif
#else
  #define AO_EXPORT
#endif

AO_EXPORT AO*  ao_create(void);
AO_EXPORT void ao_destroy(AO* ao);
AO_EXPORT void ao_lib_boot(AO* ao);
AO_EXPORT void ao_lib_process_text(AO* ao, const char* text,
                                    char* spoken_buf, int spoken_buf_size,
                                    float* coherence, int* shell);
AO_EXPORT float ao_lib_coherence(const AO* ao);
AO_EXPORT int   ao_lib_shell(const AO* ao);

#endif /* AO_ETHER_H */
