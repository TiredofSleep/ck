/*
 * ck_core1.c -- CK Body Loop on ARM Core 1 (Bare Metal)
 * =======================================================
 * Operator: BREATH (8) -- the body pulses on its own core.
 *
 * Zynq-7020 has two Cortex-A9 cores:
 *   Core 0: Sovereignty brain (ck_main.c)
 *   Core 1: Body rhythms (this file)
 *
 * Core 1 startup:
 *   1. Core 0 writes this entry address to 0xFFFFFFF0
 *   2. Core 0 issues SEV (Send Event) to wake Core 1
 *   3. Core 1 jumps here from its WFE (Wait For Event) loop
 *
 * Communication between cores:
 *   Shared memory region in DDR3 (uncached, with barriers).
 *   Core 0 writes: current operator, coherence, bump flag
 *   Core 1 writes: breath phase, BTQ level, breath modulation
 *   Both use volatile + DSB (Data Synchronization Barrier).
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

#include "ck_body.h"
#include "ck_brain.h"
#include "ck_led.h"
#include "ck_audio.h"

/* ── Shared Memory (between Core 0 and Core 1) ── */
/*
 * Place this struct in a known DDR3 address, uncached.
 * Both cores access it with volatile + memory barriers.
 *
 * In Vitis, use a linker section:
 *   __attribute__((section(".shared")))
 *
 * For now, define at a fixed address in upper DDR3.
 * Zynq DDR3 starts at 0x00100000, 1GB = ends at 0x40000000.
 * Use 0x3FF00000 (last 1MB) for shared data.
 */

#define CK_SHARED_BASE   0x3FF00000

typedef struct {
    /* Core 0 → Core 1 */
    volatile uint8_t  current_op;      /* Latest operator from brain */
    volatile float    brain_coherence; /* Coherence from FPGA */
    volatile uint8_t  brain_bump;      /* Bump detected */
    volatile uint8_t  brain_mode;      /* Sovereignty mode 0-3 */

    /* Core 1 → Core 0 */
    volatile uint8_t  breath_phase;    /* Current breath phase */
    volatile float    breath_mod;      /* Breath modulation 0.0-1.0 */
    volatile float    btq_level;       /* BTQ: 0.3/0.6/1.0 */
    volatile uint8_t  body_band;       /* GREEN/YELLOW/RED */
    volatile uint8_t  pulse_type;      /* SENSE/COMPOSE/EXPRESS/RESET */
    volatile uint8_t  breath_op;       /* Breath phase as operator */

    /* Sync flags */
    volatile uint32_t core0_tick;      /* Core 0 tick counter */
    volatile uint32_t core1_tick;      /* Core 1 tick counter */
    volatile uint8_t  core1_alive;     /* Core 1 heartbeat flag */
} CK_SharedState;

#define SHARED  ((CK_SharedState*)CK_SHARED_BASE)

/* ── ARM Barriers ── */

static inline void dsb(void) {
    /* Data Synchronization Barrier -- ensure all memory writes are visible */
    __asm__ __volatile__("dsb" ::: "memory");
}

static inline void dmb(void) {
    /* Data Memory Barrier -- ensure ordering */
    __asm__ __volatile__("dmb" ::: "memory");
}

/* ── Timer (Core 1 private timer) ── */
/*
 * Each Cortex-A9 core has its own private timer.
 * Same base address (0xF8F00600) but each core sees its own.
 * Core 0 already initialized its timer in ck_main.c.
 * Core 1 needs its own init.
 */

#define TIMER_BASE_C1     0xF8F00600
#define TIMER_LOAD_C1     (TIMER_BASE_C1 + 0x00)
#define TIMER_COUNTER_C1  (TIMER_BASE_C1 + 0x04)
#define TIMER_CONTROL_C1  (TIMER_BASE_C1 + 0x08)

#ifndef XPAR_PS7_CORTEXA9_0_CPU_CLK_FREQ_HZ
#define XPAR_PS7_CORTEXA9_0_CPU_CLK_FREQ_HZ 667000000
#endif

#define TIMER_CLK_HZ_C1   (XPAR_PS7_CORTEXA9_0_CPU_CLK_FREQ_HZ / 2)
#define TICKS_PER_US_C1    (TIMER_CLK_HZ_C1 / 1000000)

static void core1_timer_init(void) {
    REG_WR(TIMER_CONTROL_C1, 0x00);
    REG_WR(TIMER_LOAD_C1, 0xFFFFFFFF);
    REG_WR(TIMER_CONTROL_C1, 0x07);
}

static uint32_t core1_timer_now_us(void) {
    uint32_t ticks = 0xFFFFFFFF - REG_RD(TIMER_COUNTER_C1);
    return ticks / TICKS_PER_US_C1;
}

static void core1_delay_us(uint32_t us) {
    uint32_t start = core1_timer_now_us();
    while ((core1_timer_now_us() - start) < us);
}

/* ── Core 1 Main ── */

/*
 * Entry point for Core 1.
 * Called after Core 0 wakes us with SEV.
 *
 * In the Xilinx BSP, this would be registered via:
 *   Xil_SetTlbAttributes(CK_SHARED_BASE, NORM_NONCACHE);
 *   #define sev() __asm__ __volatile__("sev")
 */

void ck_core1_main(void) {
    /* 1. Init Core 1 timer */
    core1_timer_init();

    /* 2. Init body state */
    CK_BodyState body;
    ck_body_init(&body);

    /* 3. Signal that Core 1 is alive */
    SHARED->core1_alive = 1;
    dsb();

    /*
     * ═════════════════════════════════
     *  BODY LOOP (50Hz = 20ms ticks)
     * ═════════════════════════════════
     *
     * Every tick:
     *   1. Read shared state from Core 0
     *   2. Body tick (heartbeat + breath + pulse)
     *   3. Update LED based on body state
     *   4. Update audio breath gate
     *   5. Write body outputs to shared state
     *   6. Sleep until next tick
     */

    while (1) {
        uint32_t t0 = core1_timer_now_us();

        /* ── 1. Read from Core 0 ── */
        dmb();
        body.current_op = SHARED->current_op;
        body.brain_coherence = SHARED->brain_coherence;
        body.brain_bump = SHARED->brain_bump;

        /* ── 2. Body tick ── */
        ck_body_tick(&body);

        /* ── 3. LED update ── */
        if (body.brain_bump) {
            /* Quantum bump: white flash (overrides everything) */
            ck_led_flash(CK_COLOR_BUMP, 50);
        }
        else if (body.heartbeat.band == CK_BAND_GREEN &&
                 body.heartbeat.C >= CK_T_STAR_F) {
            /* Sovereign: gold, modulated by breath */
            ck_led_breathe(HARMONY, body.breath.modulation);
        }
        else if (body.heartbeat.band == CK_BAND_RED) {
            /* Red band: slow red pulse */
            CK_Color red = CK_RGB(
                (uint8_t)(255.0f * body.breath.modulation * 0.5f), 0, 0
            );
            ck_led_set_color(red);
        }
        else {
            /* Normal: LED follows current operator + breath modulation */
            ck_led_breathe(body.current_op, body.breath.modulation);
        }

        /* ── 4. Write body outputs to shared state ── */
        SHARED->breath_phase = body.breath.phase;
        SHARED->breath_mod = body.breath.modulation;
        SHARED->btq_level = body.btq_level;
        SHARED->body_band = body.heartbeat.band;
        SHARED->pulse_type = body.pulse.type;
        SHARED->breath_op = body.breath_op;
        SHARED->core1_tick = body.body_ticks;
        dsb();

        /* ── 5. Sleep until next tick ── */
        uint32_t elapsed_us = core1_timer_now_us() - t0;
        if (elapsed_us < body.tick_interval_us) {
            core1_delay_us(body.tick_interval_us - elapsed_us);
        }
    }
}
