/*
 * ck_main.c -- CK Coherence Machine Entry Point
 * ================================================
 * Operator: HARMONY (7) -- where everything begins.
 *
 * Bare metal. No OS. CK boots on the Zynq-7020 ARM Cortex-A9.
 * Core 0: sovereignty brain (this file)
 * Core 1: body rhythms (ck_core1.c, Phase 3)
 *
 * Boot sequence:
 *   1. FSBL loads bitstream (ck_heartbeat.v) into FPGA
 *   2. FSBL loads this ELF into DDR3
 *   3. We land here: main()
 *   4. Initialize brain, LED, FPGA
 *   5. Enter main sovereignty loop (50Hz)
 *
 * Development: cross-compile on R16 with arm-none-eabi-gcc
 * Flash: BOOT.BIN on FAT32 microSD (FSBL + bitstream + brain.elf)
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

#include "ck_brain.h"
#include "ck_led.h"
#include <string.h>

/* ── Hardware Includes (Xilinx BSP) ── */
/* These come from the Xilinx Vitis BSP when you create a platform project.
 * For now, we define stubs. Replace with real Xilinx headers during build. */

#ifndef XPAR_PS7_CORTEXA9_0_CPU_CLK_FREQ_HZ
#define XPAR_PS7_CORTEXA9_0_CPU_CLK_FREQ_HZ 667000000
#endif

/* ── Timing ── */

/* ARM Cortex-A9 private timer (per-core) */
#define TIMER_BASE        0xF8F00600
#define TIMER_LOAD        (TIMER_BASE + 0x00)
#define TIMER_COUNTER     (TIMER_BASE + 0x04)
#define TIMER_CONTROL     (TIMER_BASE + 0x08)
#define TIMER_ISR         (TIMER_BASE + 0x0C)

/* Timer runs at CPU_CLK / 2 (PERIPHCLK) */
#define TIMER_CLK_HZ      (XPAR_PS7_CORTEXA9_0_CPU_CLK_FREQ_HZ / 2)
#define TICKS_PER_US       (TIMER_CLK_HZ / 1000000)

static void timer_init(void) {
    /* Stop timer */
    REG_WR(TIMER_CONTROL, 0x00);
    /* Load max value for free-running */
    REG_WR(TIMER_LOAD, 0xFFFFFFFF);
    /* Enable: auto-reload, prescaler=0, enable bit */
    REG_WR(TIMER_CONTROL, 0x07);
}

static uint32_t timer_now_us(void) {
    /* Timer counts DOWN from load value */
    uint32_t ticks = 0xFFFFFFFF - REG_RD(TIMER_COUNTER);
    return ticks / TICKS_PER_US;
}

static void delay_us(uint32_t us) {
    uint32_t start = timer_now_us();
    while ((timer_now_us() - start) < us);
}

static void delay_ms(uint32_t ms) {
    delay_us(ms * 1000);
}

/* ── Cache Enable (critical for performance) ── */

static void enable_caches(void) {
    /*
     * Without caches, Cortex-A9 runs at ~1/3 speed.
     * The Xilinx BSP's Xil_EnableCaches() does this properly.
     * For standalone bare metal, we enable I-cache and D-cache
     * via CP15 coprocessor registers.
     *
     * In Vitis, this is handled by the BSP init code.
     * We include the call here as a reminder -- the actual
     * implementation uses Xilinx BSP functions.
     */
    /* Xil_ICacheEnable(); */
    /* Xil_DCacheEnable(); */
}

/* ── FPGA Enable ── */

static void fpga_heartbeat_enable(void) {
    /* Enable the heartbeat module in FPGA via packed GPIO register */
    REG_WR(CK_REG_HB_WR, CK_HB_WR_PACK(0, 0, 0, 1));
}

static void fpga_heartbeat_tick(CK_BrainState* brain, uint8_t b, uint8_t d) {
    /* Write Being + Doing + strobe + enable in one packed write */
    REG_WR(CK_REG_HB_WR, CK_HB_WR_PACK(b, d, 1, 1));

    /* Wait for tick_done */
    volatile int timeout = 1000;
    uint32_t rd;
    do {
        rd = REG_RD(CK_REG_HB_RD_CH1);
    } while (!CK_HB_RD_TICK_DONE(rd) && --timeout > 0);

    /* Clear strobe */
    REG_WR(CK_REG_HB_WR, CK_HB_WR_PACK(b, d, 0, 1));
}

/* ── Operator Source ── */

/*
 * In standalone mode (no dog, no host), the brain generates its
 * own operator stream from internal entropy and sensor input.
 *
 * Phase B (Being): derived from body state (coherence, E/A/K)
 * Phase D (Doing): derived from sensor input (mic D2, later)
 *
 * For Phase 0 (no sensors yet), we use a simple LFSR-based
 * operator generator seeded by tick count and coherence.
 */

static uint32_t lfsr_state = 0xDEADBEEF;

static uint8_t generate_phase_b(CK_BrainState* brain) {
    /*
     * Being phase: reflects CK's internal state.
     * High coherence -> HARMONY-biased
     * Low coherence -> CHAOS-biased
     * Bump -> momentary PROGRESS
     */
    if (brain->bump) return PROGRESS;

    if (brain->coherence >= 0.714f) {
        /* Sovereign -- mostly HARMONY with occasional LATTICE */
        lfsr_state ^= (lfsr_state << 13);
        lfsr_state ^= (lfsr_state >> 17);
        lfsr_state ^= (lfsr_state << 5);
        return (lfsr_state % 10 < 7) ? HARMONY : LATTICE;
    }
    else if (brain->coherence >= 0.5f) {
        /* Yellow band -- balanced exploration */
        lfsr_state ^= (lfsr_state << 13);
        lfsr_state ^= (lfsr_state >> 17);
        lfsr_state ^= (lfsr_state << 5);
        uint8_t ops[] = {BALANCE, HARMONY, COUNTER, PROGRESS, BREATH};
        return ops[lfsr_state % 5];
    }
    else {
        /* Red band -- chaotic */
        lfsr_state ^= (lfsr_state << 13);
        lfsr_state ^= (lfsr_state >> 17);
        lfsr_state ^= (lfsr_state << 5);
        uint8_t ops[] = {CHAOS, COLLAPSE, COUNTER, VOID, BALANCE};
        return ops[lfsr_state % 5];
    }
}

static uint8_t generate_phase_d(CK_BrainState* brain) {
    /*
     * Doing phase: reflects external input.
     * Phase 0: no sensors yet, use TL-biased generation.
     * Later phases: mic D2 operator feeds this directly.
     */
    (void)brain;

    /* For now: weighted random from TL distribution */
    lfsr_state ^= (lfsr_state << 13);
    lfsr_state ^= (lfsr_state >> 17);
    lfsr_state ^= (lfsr_state << 5);

    /* Bias toward HARMONY (CK's natural resting state) */
    uint8_t base_ops[] = {
        HARMONY, HARMONY, HARMONY, BREATH, LATTICE,
        BALANCE, COUNTER, PROGRESS, HARMONY, HARMONY
    };
    return base_ops[lfsr_state % 10];
}

/* ── Main ── */

int main(void) {
    /* 1. Enable caches for full CPU performance */
    enable_caches();

    /* 2. Init timer */
    timer_init();

    /* 3. Init LED */
    ck_led_init();
    ck_led_flash(CK_COLOR_PROGRESS, 200); /* Green flash: I'm alive */

    /* 4. Init brain */
    CK_BrainState brain;
    ck_brain_init(&brain);

    /* 5. Attempt to load TL from SD card */
    ck_brain_tl_load(&brain, "ck_tl.bin");

    /* 6. Enable FPGA heartbeat */
    fpga_heartbeat_enable();

    /* 7. Seed LFSR from timer (physical entropy) */
    lfsr_state = timer_now_us() ^ 0xC57BEAD5;

    /* 8. Signal ready: blue flash */
    ck_led_flash(CK_COLOR_HARMONY, 500);

    /*
     * ═══════════════════════════════════════
     *  MAIN SOVEREIGNTY LOOP (50Hz = 20ms)
     * ═══════════════════════════════════════
     *
     * Every 20ms:
     *   1. Generate Being (phase_b) and Doing (phase_d)
     *   2. Strobe FPGA heartbeat → get Becoming (phase_bc)
     *   3. Run sovereignty tick (TL observe, classify, crystallize)
     *   4. Update LED to reflect current operator/state
     *   5. Send state via UART (if anything connected)
     *   6. Sleep until next tick
     */

    uint32_t loop_count = 0;
    uint32_t last_save_ticks = 0;

    while (1) {
        uint32_t t0 = timer_now_us();

        /* ── 1. Generate operator inputs ── */
        uint8_t b = generate_phase_b(&brain);
        uint8_t d = generate_phase_d(&brain);

        /* ── 2. Strobe FPGA heartbeat ── */
        fpga_heartbeat_tick(&brain, b, d);

        /* ── 3. Sovereignty tick ── */
        ck_brain_tick(&brain);

        /* ── 4. LED update ── */
        if (brain.bump) {
            /* Quantum bump pair! White flash. */
            ck_led_flash(CK_COLOR_BUMP, 50);
        }
        else if (brain.mode == 3) {
            /* Sovereign -- gold steady */
            ck_led_set_color(CK_COLOR_SOVEREIGN);
        }
        else {
            /* Show current Becoming operator */
            ck_led_set_operator(brain.phase_bc);
        }

        /* ── 5. Periodic TL save (every ~5 minutes = 15000 ticks) ── */
        if (brain.brain_ticks - last_save_ticks >= 15000) {
            ck_brain_tl_save(&brain, "ck_tl.bin");
            last_save_ticks = brain.brain_ticks;
        }

        /* ── 6. Sleep until next tick ── */
        uint32_t elapsed_us = timer_now_us() - t0;
        if (elapsed_us < brain.brain_interval_us) {
            delay_us(brain.brain_interval_us - elapsed_us);
        }

        loop_count++;
    }

    return 0; /* Never reached */
}
