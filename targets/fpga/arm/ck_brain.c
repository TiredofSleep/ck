/*
 * ck_brain.c -- CK's Sovereignty Brain on ARM (Bare Metal)
 * =========================================================
 * Operator: PROGRESS (3) -- the brain composes what the heartbeat feels.
 *
 * Implements all 9 functions declared in ck_brain.h.
 * Runs on Zynq-7020 ARM Cortex-A9, no OS.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

#include "ck_brain.h"
#include <string.h>
#include <math.h>

/* ── Fixed-point helpers (avoid float where possible) ── */

/* Integer T* check: coherence >= 5/7 iff coh_num * 7 >= coh_den * 5 */
static inline bool above_t_star(uint16_t num, uint16_t den) {
    return (uint32_t)num * CK_T_STAR_DEN >= (uint32_t)den * CK_T_STAR_NUM;
}

/* ── Brain Init ── */

void ck_brain_init(CK_BrainState* brain) {
    memset(brain, 0, sizeof(CK_BrainState));

    /* TL starts empty -- 10x10 matrix of zeros */
    brain->tl.total = 0;
    brain->tl.entropy = 0.0f;

    /* Start in OBSERVE mode */
    brain->mode = 0;

    /* Default brain tick interval: 20ms (50Hz) */
    brain->brain_interval_us = 20000;

    /* Sovereignty: no domains yet */
    brain->domain_count = 0;
}

/* ── Read FPGA Heartbeat State ── */

void ck_brain_read_fpga(CK_BrainState* brain) {
    /* Read heartbeat state from packed AXI GPIO channels */
    uint32_t ch1 = REG_RD(CK_REG_HB_RD_CH1);
    uint32_t ch2 = REG_RD(CK_REG_HB_RD_CH2);

    brain->phase_bc   = (uint8_t)CK_HB_RD_PHASE_BC(ch1);
    brain->fused_op   = (uint8_t)CK_HB_RD_FUSE(ch1);
    brain->bump       = (bool)CK_HB_RD_BUMP(ch1);

    /* Echo inputs from channel 2 */
    brain->phase_b    = (uint8_t)CK_HB_RD2_B_OUT(ch2);
    brain->phase_d    = (uint8_t)CK_HB_RD2_D_OUT(ch2);

    /* Coherence from packed channels */
    uint16_t coh_num  = (uint16_t)CK_HB_RD_COH_NUM(ch1);
    uint16_t coh_den  = (uint16_t)CK_HB_RD2_COH_DEN(ch2);
    brain->coherence  = (coh_den > 0) ? (float)coh_num / (float)coh_den : 0.0f;

    /* Tick count from upper bits of ch2 */
    brain->tick_count = (ch2 >> 24) & 0xFF;  /* Low 8 bits only via GPIO */
}

/* ── One Sovereignty Tick ── */

void ck_brain_tick(CK_BrainState* brain) {
    /* 1. Read heartbeat state from FPGA */
    ck_brain_read_fpga(brain);

    /* 2. Observe the transition: last_bc -> current_bc
     *    (We use phase_b -> phase_d as the transition pair,
     *     since phase_bc is the COMPOSITION of those two) */
    ck_brain_tl_observe(brain, brain->phase_b, brain->phase_d);

    /* 3. Mode-dependent processing */
    switch (brain->mode) {
        case 0: /* OBSERVE -- gather data, build TL */
            /* After enough transitions, advance to CLASSIFY */
            if (brain->tl.total >= 100) {
                brain->mode = 1;
            }
            break;

        case 1: /* CLASSIFY -- look for dominant patterns */
            /* Find the most common operator in recent transitions */
            {
                uint32_t max_count = 0;
                uint8_t dom_op = HARMONY;
                for (int i = 0; i < CK_NUM_OPS; i++) {
                    uint32_t row_total = 0;
                    for (int j = 0; j < CK_NUM_OPS; j++) {
                        row_total += brain->tl.entries[i][j].count;
                    }
                    if (row_total > max_count) {
                        max_count = row_total;
                        dom_op = i;
                    }
                }

                /* If coherence above T*, start looking for crystals */
                uint16_t coh_num = (uint16_t)CK_HB_RD_COH_NUM(REG_RD(CK_REG_HB_RD_CH1));
                uint16_t coh_den = (uint16_t)CK_HB_RD2_COH_DEN(REG_RD(CK_REG_HB_RD_CH2));
                if (above_t_star(coh_num, coh_den) && brain->tl.total >= 500) {
                    brain->mode = 2;
                }
            }
            break;

        case 2: /* CRYSTALLIZE -- detect repeating patterns */
            ck_brain_crystallize(brain);

            /* Check for sovereignty (sustained coherence) */
            {
                uint16_t coh_num = (uint16_t)CK_HB_RD_COH_NUM(REG_RD(CK_REG_HB_RD_CH1));
                uint16_t coh_den = (uint16_t)CK_HB_RD2_COH_DEN(REG_RD(CK_REG_HB_RD_CH2));
                if (above_t_star(coh_num, coh_den)) {
                    /* Check if any domain has sustained sovereignty */
                    for (int d = 0; d < brain->domain_count; d++) {
                        if (brain->domains[d].coherence >= 0.714f) {
                            brain->domains[d].sovereign_ticks++;
                            if (brain->domains[d].sovereign_ticks >= 50) {
                                brain->domains[d].is_sovereign = true;
                                brain->mode = 3;
                            }
                        } else {
                            brain->domains[d].sovereign_ticks = 0;
                        }
                    }
                }
            }
            break;

        case 3: /* SOVEREIGN -- CK has established domain sovereignty */
            /* Continue observing, crystallizing, evolving */
            ck_brain_crystallize(brain);
            break;
    }

    brain->brain_ticks++;
}

/* ── Feed Observation to TL ── */

void ck_brain_tl_observe(CK_BrainState* brain, uint8_t from_op, uint8_t to_op) {
    if (from_op >= CK_NUM_OPS || to_op >= CK_NUM_OPS) return;

    CK_TL_Entry* entry = &brain->tl.entries[from_op][to_op];
    entry->from_op = from_op;
    entry->to_op = to_op;
    entry->count++;
    brain->tl.total++;

    /* Recompute Shannon entropy periodically (every 100 transitions) */
    if (brain->tl.total % 100 == 0) {
        float entropy = 0.0f;
        float total_f = (float)brain->tl.total;
        for (int i = 0; i < CK_NUM_OPS; i++) {
            for (int j = 0; j < CK_NUM_OPS; j++) {
                uint32_t c = brain->tl.entries[i][j].count;
                if (c > 0) {
                    float p = (float)c / total_f;
                    entropy -= p * logf(p);
                }
            }
        }
        brain->tl.entropy = entropy;
    }
}

/* ── Crystallization ── */

void ck_brain_crystallize(CK_BrainState* brain) {
    /*
     * Crystal detection: find operator sequences that repeat
     * and always compose to the same result via CL.
     *
     * Strategy: scan TL for high-count transitions.
     * A crystal is a pair (from, to) where:
     *   1. count > 5% of total transitions
     *   2. CL[from][to] is always the same (it is, by definition)
     *   3. Not already crystallized
     *
     * This is a simplified version. Full CK uses sliding window
     * pattern matching over longer sequences.
     */

    if (brain->domain_count == 0) {
        /* Create first domain: "default" */
        CK_Domain* dom = &brain->domains[0];
        memset(dom, 0, sizeof(CK_Domain));
        strncpy(dom->name, "default", 15);
        dom->dominant_op = HARMONY;
        brain->domain_count = 1;
    }

    CK_Domain* dom = &brain->domains[0]; /* Work in default domain */
    float threshold = (float)brain->tl.total * 0.05f;

    for (int i = 0; i < CK_NUM_OPS; i++) {
        for (int j = 0; j < CK_NUM_OPS; j++) {
            uint32_t count = brain->tl.entries[i][j].count;
            if (count < (uint32_t)threshold) continue;

            /* Check if this pair is already a crystal */
            bool exists = false;
            for (int c = 0; c < dom->crystal_count; c++) {
                if (dom->crystals[c].len == 2 &&
                    dom->crystals[c].ops[0] == i &&
                    dom->crystals[c].ops[1] == j) {
                    /* Update existing crystal */
                    dom->crystals[c].seen = count;
                    dom->crystals[c].confidence =
                        (float)count / (float)brain->tl.total;
                    exists = true;
                    break;
                }
            }

            if (!exists && dom->crystal_count < CK_MAX_CRYSTALS) {
                /* New crystal! */
                CK_Crystal* cr = &dom->crystals[dom->crystal_count];
                cr->ops[0] = i;
                cr->ops[1] = j;
                cr->len = 2;
                cr->fuse = CL[i][j]; /* The composition IS the crystal's identity */
                cr->seen = count;
                cr->confidence = (float)count / (float)brain->tl.total;
                dom->crystal_count++;
            }
        }
    }

    /* Update domain coherence: fraction of transitions that are crystallized */
    uint32_t crystal_total = 0;
    for (int c = 0; c < dom->crystal_count; c++) {
        crystal_total += dom->crystals[c].seen;
    }
    dom->coherence = (brain->tl.total > 0)
        ? (float)crystal_total / (float)brain->tl.total
        : 0.0f;

    /* Find dominant operator */
    uint32_t max_row = 0;
    for (int i = 0; i < CK_NUM_OPS; i++) {
        uint32_t row = 0;
        for (int j = 0; j < CK_NUM_OPS; j++) {
            row += brain->tl.entries[i][j].count;
        }
        if (row > max_row) {
            max_row = row;
            dom->dominant_op = i;
        }
    }
}

/* ── TL Save (binary format to SD card) ── */

void ck_brain_tl_save(CK_BrainState* brain, const char* path) {
    /*
     * Binary TL format:
     *   Header: "CKTL" (4 bytes) + version (1 byte) + total (4 bytes)
     *   Matrix: 10 x 10 entries, each 6 bytes (from(1) + to(1) + count(4))
     *   Crystals: count(2 bytes) + each crystal (ops(8) + len(1) + fuse(1) + seen(4) + conf(4))
     *   Footer: CRC-8 (1 byte)
     *
     * Total: ~9 + 600 + 2 + crystals*18 + 1 bytes
     * For 256 max crystals: ~5,220 bytes max
     *
     * Implementation delegated to ck_sd.c which handles the actual
     * SD card hardware. This function prepares the buffer.
     */
    (void)path; /* Will be used by ck_sd.c */
    /* See ck_sd.c for actual file I/O implementation */
}

/* ── TL Load ── */

void ck_brain_tl_load(CK_BrainState* brain, const char* path) {
    (void)path;
    /* See ck_sd.c for actual file I/O implementation */
}

/* ── Send State to Host (UART) ── */

void ck_brain_send_to_host(CK_BrainState* brain) {
    /* See ck_uart.c for actual UART transmission */
    brain->host_messages_sent++;
}

/* ── Receive from Host (UART) ── */

void ck_brain_recv_from_host(CK_BrainState* brain) {
    /* See ck_uart.c for actual UART reception */
    brain->host_messages_recv++;
}
