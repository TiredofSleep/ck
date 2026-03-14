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
#include "ck_ears.h"
#include "ck_dog_steer.h"
#include "ck_usb_host.h"
#include <string.h>

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

    /* Audio / Ears */
    volatile uint8_t  ear_operator;   /* Operator from microphone D2 */
    volatile float    ear_magnitude;  /* D2 magnitude of last audio frame */
    volatile uint8_t  audio_active;   /* 1 = audio engine producing sound */

    /* Dog Steering */
    volatile uint8_t  steer_mode;     /* 0=OBSERVE, 1=BLEND, 2=OVERRIDE, 3=ESTOP */
    volatile float    gait_confidence;/* How well CK understands the gait */
    volatile uint8_t  gait_op;        /* D2 operator of overall gait pattern */

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

/* ── Bus Servo Driver ── */
/*
 * XiaoR Geek robot dog uses LewanSoul/HiWonder bus servos.
 * Protocol: half-duplex UART @ 115200 baud.
 *
 * Packet format:
 *   [0x55] [0x55] [ID] [LEN] [CMD] [PARAM...] [CHECKSUM]
 *   Checksum = ~(ID + LEN + CMD + PARAM...) & 0xFF
 *
 * Key commands:
 *   CMD 1: SERVO_MOVE_TIME_WRITE
 *     Params: [angle_low] [angle_high] [time_low] [time_high]
 *     Angle: 0-1000 (maps to 0-240 degrees)
 *     Time: milliseconds to reach position
 *
 * Servo IDs (XiaoR 4-leg, 2 DOF each):
 *   Leg 0 (FL): hip=1, knee=2
 *   Leg 1 (FR): hip=3, knee=4
 *   Leg 2 (BL): hip=5, knee=6
 *   Leg 3 (BR): hip=7, knee=8
 */

#define SERVO_CMD_MOVE  1   /* SERVO_MOVE_TIME_WRITE */
#define SERVO_MOVE_LEN  7   /* ID(1)+LEN(1)+CMD(1)+angle(2)+time(2) */
#define SERVO_IDS_PER_LEG 2

/* Servo ID mapping: leg index -> {hip_id, knee_id} */
static const uint8_t servo_ids[4][2] = {
    {1, 2},  /* Leg 0: FL */
    {3, 4},  /* Leg 1: FR */
    {5, 6},  /* Leg 2: BL */
    {7, 8},  /* Leg 3: BR */
};

/* Convert PWM microseconds (500-2500) to LewanSoul angle (0-1000) */
static uint16_t pwm_to_servo_angle(uint16_t pwm_us) {
    /* PWM 500us = 0 deg = angle 0 */
    /* PWM 2500us = 240 deg = angle 1000 */
    /* But servos only need 0-180 deg range → 500-2500 us → 0-833 */
    if (pwm_us < 500) pwm_us = 500;
    if (pwm_us > 2500) pwm_us = 2500;
    return (uint16_t)(((uint32_t)(pwm_us - 500) * 1000) / 2000);
}

/* Send one byte to servo UART (PL-side UART for bus servos) */
static void servo_uart_tx(uint8_t byte) {
    while (REG_RD(CK_SERVO_UART_SR) & CK_SERVO_UART_TXFULL);
    REG_WR(CK_SERVO_UART_TX, (uint32_t)byte);
}

/* Send a SERVO_MOVE_TIME_WRITE command to one servo */
static void servo_move(uint8_t id, uint16_t angle, uint16_t time_ms) {
    uint8_t pkt[10];
    pkt[0] = 0x55;
    pkt[1] = 0x55;
    pkt[2] = id;
    pkt[3] = SERVO_MOVE_LEN;  /* length: from here to end including checksum */
    pkt[4] = SERVO_CMD_MOVE;
    pkt[5] = angle & 0xFF;
    pkt[6] = (angle >> 8) & 0xFF;
    pkt[7] = time_ms & 0xFF;
    pkt[8] = (time_ms >> 8) & 0xFF;

    /* Checksum = ~(ID + LEN + CMD + params) & 0xFF */
    uint8_t sum = pkt[2] + pkt[3] + pkt[4] + pkt[5] + pkt[6] + pkt[7] + pkt[8];
    pkt[9] = ~sum;

    for (int i = 0; i < 10; i++) {
        servo_uart_tx(pkt[i]);
    }
}

/*
 * Read servo calibration from FPGA and command all 8 servos.
 * Called when gait_corr_valid fires (gait vortex produced new corrections).
 *
 * Move time: gated by breath modulation.
 *   High coherence (CALM breath) → slow, smooth moves (100ms)
 *   Low coherence (FRACTAL breath) → fast, jerky moves (20ms)
 */
static void servo_update_all(float breath_mod) {
    /* Strobe servo_cal to compute PWM from current gait ops */
    REG_WR(CK_REG_SERVO_UPDATE, 1);

    /* Wait for valid (should be 1 clock = immediate) */
    volatile int timeout = 100;
    while (!(REG_RD(CK_REG_SERVO_VALID) & 1) && timeout > 0) timeout--;

    /* Read calibrated PWM values for all 4 legs */
    uint32_t l0_hk = REG_RD(CK_REG_SERVO_L0_HK);
    uint32_t l1_hk = REG_RD(CK_REG_SERVO_L1_HK);
    uint32_t l2_hk = REG_RD(CK_REG_SERVO_L2_HK);
    uint32_t l3_hk = REG_RD(CK_REG_SERVO_L3_HK);

    /* Extract hip and knee PWM (12-bit each, packed) */
    uint16_t hip[4], knee[4];
    hip[0]  = l0_hk & 0xFFF;         knee[0] = (l0_hk >> 16) & 0xFFF;
    hip[1]  = l1_hk & 0xFFF;         knee[1] = (l1_hk >> 16) & 0xFFF;
    hip[2]  = l2_hk & 0xFFF;         knee[2] = (l2_hk >> 16) & 0xFFF;
    hip[3]  = l3_hk & 0xFFF;         knee[3] = (l3_hk >> 16) & 0xFFF;

    /* Move time: breath-modulated. Calm = slow (100ms), fractal = fast (20ms) */
    uint16_t move_ms = (uint16_t)(20 + breath_mod * 80);

    /* Command all 8 servos */
    for (int leg = 0; leg < 4; leg++) {
        servo_move(servo_ids[leg][0], pwm_to_servo_angle(hip[leg]),  move_ms);
        servo_move(servo_ids[leg][1], pwm_to_servo_angle(knee[leg]), move_ms);
    }
}

/* E-stop: center all servos immediately */
static void servo_estop(void) {
    for (int leg = 0; leg < 4; leg++) {
        servo_move(servo_ids[leg][0], 500, 0);  /* angle 500 = center */
        servo_move(servo_ids[leg][1], 500, 0);
    }
}

/* ── Core 1 Main ── */

/*
 * Entry point for Core 1.
 * Called after Core 0 wakes us with SEV.
 *
 * Runs two interleaved loops:
 *   Body rhythms: breath, pulse, E/A/K (50Hz)
 *   Servo driver: read gait corrections → command bus servos
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

    /* 3. Init audio engine (CK's voice) */
    CK_AudioEngine audio;
    ck_audio_init(&audio, CK_DAC_SAMPLE);

    /* 4. Init ears (CK's hearing) */
    CK_Ears ears;
    ck_ears_init(&ears, CK_MIC_SAMPLE);
    ears.mic_fifo_count_addr = CK_MIC_STATUS;
    ears.mic_fifo_read_addr  = CK_MIC_READ;

    /* 5. Init dog steering (CK observes first, then takes over) */
    CK_DogSteer steer;
    ck_dog_steer_init(&steer);

    /* 5b. Init USB host (FPGA → USB-C → dog head) */
    CK_UsbHost usb;
    ck_usb_host_init(&usb);

    /* 6. Signal that Core 1 is alive */
    SHARED->core1_alive = 1;
    SHARED->audio_active = 1;
    SHARED->steer_mode = CK_STEER_OBSERVE;
    dsb();

    /* 7. Enable gait controller (stand mode initially) */
    /* Packed: mode[1:0]=0 (stand), start[2]=0, enable[3]=1 */
    REG_WR(CK_REG_GAIT_WR, (1 << 3));

    /* 8. Don't e-stop on boot -- let the dog's existing gait run.
     * CK starts in OBSERVE mode: he watches and learns. */

    uint32_t last_gait_tick = 0;
    uint32_t audio_subsample = 0;

    /*
     * ═══════════════════════════════════════════
     *  BODY + SERVO LOOP (50Hz = 20ms ticks)
     * ═══════════════════════════════════════════
     *
     * Every tick:
     *   1. Read shared state from Core 0
     *   2. Body tick (heartbeat + breath + pulse)
     *   3. Update LED based on body state
     *   4. Audio tick (push operator tones to DAC)
     *  4b. Ears tick (read mic, D2 classify → operator)
     *   5. Servo update (gait → servo_cal → bus servos)
     *   6. Write body outputs to shared state
     *   7. Sleep until next tick
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

        /* ── 4. Audio tick (CK's voice -- operator tones) ── */
        /*
         * Audio runs at 44100 Hz, body loop at 50 Hz.
         * Each body tick = 20ms = 882 audio samples.
         * Generate a batch of samples per body tick.
         * The DAC SPI FIFO (256 deep) buffers them.
         */
        ck_audio_set_operator(&audio, body.current_op);
        ck_audio_set_breath(&audio, (float)body.breath.phase / 4.0f
                                    + (float)body.breath.beat_in_phase
                                    / (float)(body.breath.beats_per_cycle * 4));
        ck_audio_set_btq(&audio, body.btq_level);

        /* Push samples to DAC FIFO (up to 256 per tick, FIFO handles overflow) */
        for (int s = 0; s < 256; s++) {
            if (REG_RD(CK_DAC_STATUS) & CK_DAC_FIFO_FULL) break;
            ck_audio_tick(&audio);
        }

        /* ── 4b. Ears tick (CK hears -- sound → D2 → operator) ── */
        int ear_result = ck_ears_process(&ears);
        if (ear_result >= 0) {
            SHARED->ear_operator = (uint8_t)ear_result;
            SHARED->ear_magnitude = ears.d2_magnitude;
        }

        /* ── 5. Dog steering (observe → blend → override) ── */
        {
            /* Poll USB host -- handles connection, TX/RX with dog */
            ck_usb_host_poll(&usb);
            bool usb_ok = ck_usb_host_connected(&usb);

            /* Feed coherence to steering engine */
            ck_dog_steer_set_coherence(&steer,
                body.heartbeat.C, body.heartbeat.band);

            /* Read CK's desired targets from FPGA gait vortex */
            uint32_t gait_tick = REG_RD(CK_REG_GAIT_TICK);
            if (gait_tick != last_gait_tick) {
                last_gait_tick = gait_tick;

                /* Strobe servo_cal to get CK's desired positions */
                REG_WR(CK_REG_SERVO_UPDATE, 1);
                volatile int timeout = 100;
                while (!(REG_RD(CK_REG_SERVO_VALID) & 1) && timeout > 0) timeout--;

                /* Read CK's targets */
                uint32_t l0_hk = REG_RD(CK_REG_SERVO_L0_HK);
                uint32_t l1_hk = REG_RD(CK_REG_SERVO_L1_HK);
                uint32_t l2_hk = REG_RD(CK_REG_SERVO_L2_HK);
                uint32_t l3_hk = REG_RD(CK_REG_SERVO_L3_HK);

                /* Set CK's desired targets in steering engine */
                ck_dog_steer_set_target(&steer, 0, l0_hk & 0xFFF);
                ck_dog_steer_set_target(&steer, 1, (l0_hk >> 16) & 0xFFF);
                ck_dog_steer_set_target(&steer, 2, l1_hk & 0xFFF);
                ck_dog_steer_set_target(&steer, 3, (l1_hk >> 16) & 0xFFF);
                ck_dog_steer_set_target(&steer, 4, l2_hk & 0xFFF);
                ck_dog_steer_set_target(&steer, 5, (l2_hk >> 16) & 0xFFF);
                ck_dog_steer_set_target(&steer, 6, l3_hk & 0xFFF);
                ck_dog_steer_set_target(&steer, 7, (l3_hk >> 16) & 0xFFF);
            }

            /* Read dog's actual servo positions via USB (CMD 0x1C).
             * Request one servo per tick (round-robin) to avoid
             * flooding the bus. Response parsed from USB RX buffer. */
            if (usb_ok) {
                static uint8_t readback_id = 0;

                /* Request position for next servo */
                ck_usb_servo_read_pos(&usb, readback_id + 1);

                /* Parse any position responses from RX buffer */
                uint8_t rx_buf[32];
                uint16_t rx_len = ck_usb_host_rx(&usb, rx_buf, sizeof(rx_buf));
                for (uint16_t p = 0; p + 7 < rx_len; p++) {
                    /* Look for response: [0x55][0x55][ID][5][0x1C][pos_lo][pos_hi][csum] */
                    if (rx_buf[p] == 0x55 && rx_buf[p+1] == 0x55 &&
                        rx_buf[p+3] == 5 && rx_buf[p+4] == 0x1C) {
                        uint8_t sid = rx_buf[p+2];
                        uint16_t pos = rx_buf[p+5] | ((uint16_t)rx_buf[p+6] << 8);
                        if (sid >= 1 && sid <= 8) {
                            ck_dog_steer_observe_servo(&steer, sid - 1, pos);
                        }
                        p += 7;  /* Skip past this packet */
                    }
                }

                readback_id = (readback_id + 1) % 8;
            }

            /* Run steering tick -- decides mode + computes output */
            uint8_t mode = ck_dog_steer_tick(&steer);

            /* Send blended output to servos.
             * Route through USB if connected, fall back to PL UART. */
            if (mode != CK_STEER_ESTOP) {
                uint16_t move_ms = (uint16_t)(20 + body.breath.modulation * 80);
                for (int leg = 0; leg < 4; leg++) {
                    uint16_t hip_out  = ck_dog_steer_get_output(&steer, leg * 2);
                    uint16_t knee_out = ck_dog_steer_get_output(&steer, leg * 2 + 1);

                    if (usb_ok) {
                        /* USB path: FPGA → USB-C → dog controller */
                        ck_usb_servo_move(&usb, servo_ids[leg][0],
                                          pwm_to_servo_angle(hip_out), move_ms);
                        ck_usb_servo_move(&usb, servo_ids[leg][1],
                                          pwm_to_servo_angle(knee_out), move_ms);
                    } else {
                        /* Fallback: PL UART on JM2 (direct wire) */
                        servo_move(servo_ids[leg][0],
                                   pwm_to_servo_angle(hip_out), move_ms);
                        servo_move(servo_ids[leg][1],
                                   pwm_to_servo_angle(knee_out), move_ms);
                    }
                }
            } else if (usb_ok) {
                /* E-STOP through USB */
                ck_usb_servo_estop(&usb);
            }

            /* Re-enable from ESTOP when coherence recovers */
            if (mode == CK_STEER_ESTOP &&
                body.heartbeat.band == CK_BAND_GREEN) {
                steer.mode = CK_STEER_OBSERVE;  /* Back to watching */
                REG_WR(CK_REG_GAIT_WR, (1 << 3)); /* re-enable gait */
            }
        }

        /* ── 6. Write body outputs to shared state ── */
        SHARED->breath_phase = body.breath.phase;
        SHARED->breath_mod = body.breath.modulation;
        SHARED->btq_level = body.btq_level;
        SHARED->body_band = body.heartbeat.band;
        SHARED->pulse_type = body.pulse.type;
        SHARED->breath_op = body.breath_op;
        SHARED->steer_mode = steer.mode;
        SHARED->gait_confidence = steer.gait_confidence;
        SHARED->gait_op = steer.gait_pattern_op;
        SHARED->core1_tick = body.body_ticks;
        dsb();

        /* ── 7. Sleep until next tick ── */
        uint32_t elapsed_us = core1_timer_now_us() - t0;
        if (elapsed_us < body.tick_interval_us) {
            core1_delay_us(body.tick_interval_us - elapsed_us);
        }
    }
}
