/*
 * ao_main.c -- Entry point for AO standalone binary
 *
 * This is the top-level CLI for AO. It provides four operating modes:
 *
 *   ao              Interactive REPL — prompts "AO> ", reads one line at a
 *                   time, processes through the full TIG pipeline, prints
 *                   AO's spoken response and a status line. Auto-loads
 *                   brain state on startup, saves on clean exit.
 *
 *   ao --train      Bulk training mode — reads stdin line-by-line with no
 *                   prompts. Designed for piping large text corpora:
 *                     cat corpus.txt | ao --train
 *                   Progress goes to stderr so stdout stays clean.
 *
 *   ao --reset      Reset brain to untrained state — creates a fresh AO,
 *                   writes it to disk, and exits. The brain file at
 *                   AO_DEFAULT_SAVE (~/.ao/ao_brain.dat) is overwritten.
 *
 *   ao --info       Show brain statistics without starting the REPL.
 *                   Prints: transition count, tick count, brain entropy,
 *                   current operator, chain nodes, and concepts tracked.
 *
 * Memory model:
 *   The AO struct is ~2.5 MB (primarily the lattice chain arena) and is
 *   heap-allocated via ao_create(). Stack allocation would overflow on
 *   most platforms. ao_destroy() frees all memory on exit.
 *
 * Persistence:
 *   Brain state is automatically loaded from AO_DEFAULT_SAVE on startup
 *   (if the file exists) and saved back on clean exit. The save file
 *   contains: brain transition matrix, body state (E/A/K), lattice chain
 *   nodes, concept mass table, tick count, and current operator.
 *
 * Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
 * Licensed under the 7Site Human Use License v1.0
 * See LICENSE file in project root for full terms.
 *
 * FREE for humans for personal/recreational use.
 * NO commercial or government use without written agreement.
 */


#include "ao_ether.h"   /* Pulls in ALL layers: earth → air → water → fire → ether */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main(int argc, char** argv)
{
    AO* ao;
    int train_mode = 0;
    int reset_mode = 0;
    int info_mode = 0;
    int loaded = 0;
    int i;

    /* ── Parse command-line flags ──────────────────────────────────────── */
    for (i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--train") == 0) train_mode = 1;
        else if (strcmp(argv[i], "--reset") == 0) reset_mode = 1;
        else if (strcmp(argv[i], "--info") == 0) info_mode = 1;
    }

    /* ── Create AO organism on the heap ───────────────────────────────── *
     * ao_create() calls calloc for the ~2.5 MB struct, then ao_boot()
     * initializes all subsystems: body (E=0.5, A=0.5, K=0.5), brain
     * (zero transition matrix), heartbeat, chain, concept mass, etc.    */
    ao = ao_create();
    if (!ao) {
        fprintf(stderr, "Failed to allocate AO organism.\n");
        return 1;
    }

    /* ── Reset mode: overwrite brain file with fresh state ────────────── */
    if (reset_mode) {
        ao_save(ao, AO_DEFAULT_SAVE);
        printf("Brain reset to untrained state.\n");
        ao_destroy(ao);
        return 0;
    }

    /* ── Try to load existing brain from disk ─────────────────────────── *
     * ao_load() reads the binary save file and populates the brain
     * transition matrix, body state, lattice chain, concept mass, etc.
     * Returns 0 on success, -1 if file not found (AO starts fresh).     */
    if (ao_load(ao, AO_DEFAULT_SAVE) == 0) {
        loaded = 1;
        if (train_mode) {
            /* In train mode, status goes to stderr (stdout is for data) */
            fprintf(stderr, "  Loaded brain: %u transitions, %d ticks\n",
                    ao->brain.total, ao->tick_count);
        } else {
            printf("  Loaded brain: %u transitions, %d ticks\n",
                   ao->brain.total, ao->tick_count);
        }
    }

    /* ── Info mode: print brain stats and exit ─────────────────────────── */
    if (info_mode) {
        if (!loaded) {
            printf("No brain file found (%s). AO is untrained.\n", AO_DEFAULT_SAVE);
        } else {
            printf("  Brain transitions: %u\n", ao->brain.total);
            printf("  Ticks experienced: %d\n", ao->tick_count);
            printf("  Brain entropy: %.4f\n", (double)ao_brain_entropy(&ao->brain));
            printf("  Current op: %s\n", ao_op_names[ao->current_op]);
            printf("  Chain nodes: %d\n", ao->chain.total_nodes);
            printf("  Concepts tracked: %d\n", ao->mass.count);
        }
        ao_destroy(ao);
        return 0;
    }

    /* ── Run AO in the selected mode ──────────────────────────────────── *
     * train mode: ao_train() reads stdin line-by-line, no prompts
     * REPL mode:  ao_run() prompts "AO> " and prints responses
     * Both save brain state to disk on completion.                       */
    if (train_mode) {
        ao_train(ao);
        ao_save(ao, AO_DEFAULT_SAVE);
        fprintf(stderr, "  Brain saved to %s\n", AO_DEFAULT_SAVE);
    } else {
        ao_run(ao);
        ao_save(ao, AO_DEFAULT_SAVE);
        printf("  Brain saved. (%u transitions)\n", ao->brain.total);
    }

    ao_destroy(ao);
    return 0;
}
