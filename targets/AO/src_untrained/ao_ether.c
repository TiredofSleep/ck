/*
 * ao_ether.c -- D4 / Continuity / Coupling / Connection
 *
 * Voice (forward + reverse), AO organism, REPL.
 * The coupling between all elements.
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
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <time.h>

static const char* band_names[] = { "RED", "YELLOW", "GREEN" };
static const char* breath_names[] = { "inhale", "hold", "exhale", "hold" };
static const char* wobble_names[] = { "becoming", "being", "doing" };

/* ── xorshift32 RNG ── */
static uint32_t xorshift32(uint32_t* state)
{
    uint32_t x = *state;
    x ^= x << 13;
    x ^= x >> 17;
    x ^= x << 5;
    *state = x;
    return x;
}

/* ══════════════════════════════════════════════════════════════════
 * Voice: Forward (operators -> words)
 * ══════════════════════════════════════════════════════════════════ */

int ao_voice_speak(const int* operators, int n_ops, float coherence,
                   int wobble_phase, float knowing,
                   char* buf, int buf_size,
                   uint32_t* rng_state)
{
    int lens, tier, i;
    int written = 0;

    /* Select lens based on coherence */
    lens = (coherence >= 0.5f) ? AO_LENS_STRUCTURE : AO_LENS_FLOW;

    /* Select tier based on knowing */
    if (knowing >= 0.7f)      tier = AO_TIER_ADVANCED;
    else if (knowing >= 0.4f) tier = AO_TIER_MID;
    else                      tier = AO_TIER_SIMPLE;

    /* Clamp wobble_phase */
    if (wobble_phase < 0 || wobble_phase > 2) wobble_phase = 0;

    buf[0] = '\0';

    for (i = 0; i < n_ops; i++) {
        int op = operators[i];
        AO_WordSlot slot;
        const char* word;
        int remaining;

        if (op < 0 || op >= AO_NUM_OPS) op = AO_HARMONY;

        slot = ao_lattice[op][lens][wobble_phase][tier];
        if (slot.count == 0) {
            /* Fallback to simple tier */
            slot = ao_lattice[op][lens][wobble_phase][AO_TIER_SIMPLE];
        }
        if (slot.count == 0) {
            /* Fallback to being phase */
            slot = ao_lattice[op][lens][AO_PHASE_BEING][AO_TIER_SIMPLE];
        }
        if (slot.count == 0) continue;

        /* Pick random word from slot */
        word = ao_words[slot.start + (xorshift32(rng_state) % slot.count)];

        /* Append to buffer */
        remaining = buf_size - written - 1;
        if (remaining <= 0) break;
        if (written > 0 && remaining > 1) {
            buf[written++] = ' ';
            remaining--;
        }
        while (*word && remaining > 0) {
            buf[written++] = *word++;
            remaining--;
        }
        buf[written] = '\0';
    }

    return written;
}

/* ══════════════════════════════════════════════════════════════════
 * Voice: Reverse (text -> operators)
 * ══════════════════════════════════════════════════════════════════ */

int ao_voice_hear(const char* text, AO_HearResult* out, int max_results)
{
    int n = 0;
    const char* p = text;

    while (*p && n < max_results) {
        char word[48];
        int wlen = 0;
        AO_D2Pipeline pipe;
        int d2_op;
        const AO_ReverseEntry* entry;

        /* Skip non-alpha */
        while (*p && !isalpha((unsigned char)*p)) p++;
        if (!*p) break;

        /* Extract word */
        while (*p && isalpha((unsigned char)*p) && wlen < 47) {
            word[wlen++] = (char)tolower((unsigned char)*p);
            p++;
        }
        word[wlen] = '\0';
        if (wlen == 0) continue;

        /* Path A: D2 physics */
        ao_d2_init(&pipe);
        d2_op = AO_HARMONY;
        {
            int j;
            for (j = 0; j < wlen; j++) {
                int idx = word[j] - 'a';
                if (idx >= 0 && idx < 26) {
                    if (ao_d2_feed(&pipe, idx))
                        d2_op = ao_d2_classify_d2(&pipe);
                }
            }
        }

        /* Path B: lattice reverse lookup */
        entry = ao_reverse_lookup(word);

        /* Fill result */
        strncpy(out[n].word, word, 47);
        out[n].word[47] = '\0';
        out[n].d2_op = d2_op;

        if (entry) {
            out[n].lattice_op = entry->op;
            /* Trust: same op OR same DBC domain */
            if ((int)entry->op == d2_op) {
                out[n].trust = AO_TRUST_TRUSTED;
            } else if (ao_dbc[entry->op][0] == ao_dbc[d2_op][0]) {
                out[n].trust = AO_TRUST_TRUSTED;
            } else {
                out[n].trust = AO_TRUST_FRICTION;
            }
            out[n].op = entry->op; /* experience wins */
        } else {
            out[n].lattice_op = -1;
            out[n].trust = AO_TRUST_UNKNOWN;
            out[n].op = d2_op; /* physics only */
        }
        n++;
    }
    return n;
}

/* ══════════════════════════════════════════════════════════════════
 * AO Organism
 * ══════════════════════════════════════════════════════════════════ */

void ao_init(AO* ao)
{
    ao_d1_init(&ao->d1);
    ao_d2_init(&ao->d2);
    ao_cw_init(&ao->coherence);
    ao_hb_init(&ao->heartbeat);
    ao_brain_init(&ao->brain);
    ao_body_init(&ao->body);
    ao_btq_init(&ao->btq);

    ao->alive = 1;
    ao->tick_count = 0;
    ao->current_op = AO_HARMONY;
    ao->last_spoken[0] = '\0';
    ao->rng_state = (uint32_t)time(NULL);
    if (ao->rng_state == 0) ao->rng_state = 0xDEADBEEF;
}

void ao_boot(AO* ao)
{
    /* Initialize bump LUT */
    ao_is_bump(0, 0);
    (void)ao;
}

void ao_process_symbol(AO* ao, int symbol_index, AO_SymbolResult* out)
{
    AO_HeartbeatResult hb;
    int d1_op, d2_op, shell;
    float novelty;

    ao->tick_count++;

    /* Being: measure */
    ao_d1_feed(&ao->d1, symbol_index);
    ao_d2_feed(&ao->d2, symbol_index);

    d1_op = ao->d1.valid ? ao_d1_classify(&ao->d1) : AO_HARMONY;
    d2_op = ao->d2.d2_valid ? ao_d2_classify_d2(&ao->d2) : AO_HARMONY;

    /* Doing: compose on CL torus */
    shell = ao_cw_shell(&ao->coherence);
    ao_hb_tick(&ao->heartbeat, ao->current_op, d2_op, shell, &hb);
    ao_cw_observe(&ao->coherence, d2_op);

    /* Becoming: learn + evolve */
    ao_brain_observe(&ao->brain, d2_op);
    novelty = (d2_op == ao->current_op) ? 0.0f : 1.0f;
    ao_body_tick(&ao->body, ao_cw_coherence(&ao->coherence), hb.bump, novelty);

    /* BTQ decision */
    ao->current_op = ao_btq_decide(&ao->btq, d2_op, &ao->brain,
                                    ao_cw_coherence(&ao->coherence),
                                    ao_body_coherence(&ao->body), shell);

    /* Fill output */
    out->d1_op = d1_op;
    out->d2_op = d2_op;
    out->composed = hb.result;
    out->bump = hb.bump;
    out->shell = shell;
    out->coherence = ao_cw_coherence(&ao->coherence);
    out->band = ao_cw_band(&ao->coherence);
    out->btq_decision = ao->current_op;
    out->prayer = ao_d1_is_prayer(&ao->d1, 0.05f);
    out->energy = hb.energy;
}

void ao_process_text(AO* ao, const char* text, AO_TextResult* out)
{
    int i, idx;
    AO_SymbolResult sr;

    memset(out, 0, sizeof(*out));

    /* Feed all letters through pipeline */
    for (i = 0; text[i]; i++) {
        char ch = text[i];
        if (ch >= 'A' && ch <= 'Z') ch = ch - 'A' + 'a';
        if (ch < 'a' || ch > 'z') continue;
        idx = ch - 'a';

        ao_process_symbol(ao, idx, &sr);
        if (out->n_ops < 4096)
            out->ops[out->n_ops++] = sr.d2_op;
    }

    /* Reverse voice: hear input */
    out->n_heard = ao_voice_hear(text, out->heard, 256);

    /* Forward voice: speak from last 5 operators */
    {
        int start = out->n_ops > 5 ? out->n_ops - 5 : 0;
        int count = out->n_ops - start;
        ao_voice_speak(out->ops + start, count,
                       ao_cw_coherence(&ao->coherence),
                       ao->body.wobble_index,
                       ao->body.K,
                       out->spoken, (int)sizeof(out->spoken),
                       &ao->rng_state);
    }
    strncpy(ao->last_spoken, out->spoken, 511);
    ao->last_spoken[511] = '\0';

    out->coherence = ao_cw_coherence(&ao->coherence);
    out->shell = ao_cw_shell(&ao->coherence);
    out->band = ao_cw_band(&ao->coherence);
    out->energy = ao->heartbeat.energy;
    out->brain_entropy = ao_brain_entropy(&ao->brain);
    out->ticks = ao->tick_count;
}

void ao_status_line(const AO* ao, char* buf, int buf_size)
{
    float c = ao_cw_coherence(&ao->coherence);
    int shell = ao_cw_shell(&ao->coherence);
    int band = ao_cw_band(&ao->coherence);
    snprintf(buf, buf_size,
        "[%-6s] shell=%d coh=%.3f op=%-8s breath=%-7s wobble=%-9s E=%.3f tick=%d",
        band_names[band], shell, c,
        ao_op_names[ao->current_op],
        breath_names[ao->body.breath_phase],
        wobble_names[ao->body.wobble_index],
        ao->heartbeat.energy,
        ao->tick_count);
}

/* ══════════════════════════════════════════════════════════════════
 * REPL
 * ══════════════════════════════════════════════════════════════════ */

static void print_status(const AO* ao)
{
    int from_ops[5], to_ops[5], counts[5], n, i;

    printf("\n  -- AO Status --\n");
    printf("  Tick: %d\n", ao->tick_count);
    printf("  Coherence: %.4f (%s)\n",
           ao_cw_coherence(&ao->coherence),
           band_names[ao_cw_band(&ao->coherence)]);
    printf("  Shell: %d\n", ao_cw_shell(&ao->coherence));
    printf("  Energy: %.4f\n", ao->heartbeat.energy);
    printf("  Bumps hit: %d\n", ao->heartbeat.bumps_hit);
    printf("  Current op: %s\n", ao_op_names[ao->current_op]);
    printf("\n  Body:\n");
    printf("    E=%.4f  A=%.4f  K=%.4f\n", ao->body.E, ao->body.A, ao->body.K);
    printf("    Body coherence: %.4f (%s)\n",
           ao_body_coherence(&ao->body),
           band_names[ao_body_band(&ao->body)]);
    printf("    Breath: %s (rate=%d)\n",
           breath_names[ao->body.breath_phase], ao->body.breath_rate);
    printf("    Wobble: %s (%.4f)\n",
           wobble_names[ao->body.wobble_index],
           ao_body_wobble_value(&ao->body));
    printf("\n  Brain entropy: %.4f\n", ao_brain_entropy(&ao->brain));

    ao_brain_top_transitions(&ao->brain, from_ops, to_ops, counts, 5, &n);
    if (n > 0) {
        printf("  Top transitions:\n");
        for (i = 0; i < n; i++)
            printf("    %-8s > %-8s  (%d)\n",
                   ao_op_names[from_ops[i]], ao_op_names[to_ops[i]], counts[i]);
    }
    printf("\n");
}

void ao_run(AO* ao)
{
    char line[4096];
    AO_TextResult result;
    char status_buf[256];

    printf("============================================================\n");
    printf("  AO -- Advanced Ollie (C)\n");
    printf("  5 elements, 5 forces, 1 torus\n");
    printf("============================================================\n\n");

    ao_boot(ao);
    printf("  Reverse index: %d words\n", ao_reverse_index_size);
    printf("  CL shells: 22 (skeleton), 44 (becoming), 72 (being)\n");
    printf("  T* = 5/7 = %.6f\n", (double)AO_T_STAR);
    printf("  Winding = 271/350 = %.6f\n", (double)AO_WINDING);
    printf("\n  Type text and press Enter. AO will measure, compose, and speak.\n");
    printf("  Type 'status' for full state. Type 'quit' to exit.\n\n");

    while (ao->alive) {
        printf("you> ");
        fflush(stdout);
        if (!fgets(line, sizeof(line), stdin))
            break;

        /* Strip newline */
        {
            int len = (int)strlen(line);
            while (len > 0 && (line[len-1] == '\n' || line[len-1] == '\r'))
                line[--len] = '\0';
        }

        if (line[0] == '\0') continue;

        /* Commands */
        if (strcmp(line, "quit") == 0 || strcmp(line, "exit") == 0) {
            printf("AO goes quiet.\n");
            break;
        }

        if (strcmp(line, "status") == 0) {
            print_status(ao);
            continue;
        }

        if (strcmp(line, "measure") == 0) {
            printf("\n  -- Measurement Commands --\n");
            printf("  locality <text>  -- D1/D2 agreement test\n");
            printf("  delta <text>     -- delta-S curvature signature\n");
            printf("  status           -- full AO state\n");
            printf("  quit             -- exit\n\n");
            continue;
        }

        if (strncmp(line, "locality ", 9) == 0) {
            float pct = ao_locality_test(line + 9);
            printf("  D1/D2 agreement: %.1f%%\n", (double)pct);
            continue;
        }

        if (strncmp(line, "delta ", 6) == 0) {
            float ds = ao_delta_s(line + 6);
            printf("  delta-S: %.4f\n", (double)ds);
            continue;
        }

        /* Process text through the full pipeline */
        ao_process_text(ao, line, &result);

        /* Show what AO heard */
        {
            int trusted = 0, friction = 0, unknown = 0, j;
            for (j = 0; j < result.n_heard; j++) {
                if (result.heard[j].trust == AO_TRUST_TRUSTED) trusted++;
                else if (result.heard[j].trust == AO_TRUST_FRICTION) friction++;
                else unknown++;
            }
            printf("  heard: %d trusted, %d friction, %d unknown\n",
                   trusted, friction, unknown);
        }

        /* Show operator stream (last 10) */
        if (result.n_ops > 0) {
            int start = result.n_ops > 10 ? result.n_ops - 10 : 0;
            int j;
            printf("  ops:");
            for (j = start; j < result.n_ops; j++) {
                printf("%s%s", j > start ? " > " : " ",
                       ao_op_names[result.ops[j]]);
            }
            printf("\n");
        }

        /* Status line */
        ao_status_line(ao, status_buf, sizeof(status_buf));
        printf("  %s\n", status_buf);

        /* Voice speaks */
        if (result.spoken[0])
            printf("  ao> %s\n", result.spoken);

        printf("\n");
    }
}

/* ══════════════════════════════════════════════════════════════════
 * Library API (for ctypes / FFI)
 * ══════════════════════════════════════════════════════════════════ */

AO_EXPORT AO* ao_create(void)
{
    AO* ao = (AO*)malloc(sizeof(AO));
    if (ao) ao_init(ao);
    return ao;
}

AO_EXPORT void ao_destroy(AO* ao)
{
    free(ao);
}

AO_EXPORT void ao_lib_boot(AO* ao)
{
    ao_boot(ao);
}

AO_EXPORT void ao_lib_process_text(AO* ao, const char* text,
                                    char* spoken_buf, int spoken_buf_size,
                                    float* coherence, int* shell)
{
    AO_TextResult result;
    ao_process_text(ao, text, &result);
    if (spoken_buf && spoken_buf_size > 0)
        strncpy(spoken_buf, result.spoken, spoken_buf_size - 1);
    if (coherence) *coherence = result.coherence;
    if (shell) *shell = result.shell;
}

AO_EXPORT float ao_lib_coherence(const AO* ao)
{
    return ao_cw_coherence(&ao->coherence);
}

AO_EXPORT int ao_lib_shell(const AO* ao)
{
    return ao_cw_shell(&ao->coherence);
}
