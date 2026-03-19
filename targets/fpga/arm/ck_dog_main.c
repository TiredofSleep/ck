/*
 * ck_dog_main.c -- CK Dog ARM Firmware (Bare-metal, Zynq-7020)
 * ============================================================
 *
 * Dual-core architecture:
 *   Core 0: CK Brain (heartbeat + BTQ + coherence monitoring)
 *   Core 1: CK Body (gait execution + servo output + sensor input)
 *
 * Both cores share state through on-chip BRAM (OCM at 0xFFFF0000).
 * PL fabric runs: heartbeat, D2, chain walker, gait vortex,
 *                 servo UART, I2C IMU, I2S mic, DAC speaker.
 *
 * ARM reads PL outputs via AXI GPIO and steers the dog body.
 * CK earns control through coherence: OBSERVE -> BLEND -> OVERRIDE.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
 */

#include <stdint.h>
#include <string.h>
#include "xparameters.h"
#include "xgpio.h"
#include "xil_printf.h"
#include "sleep.h"
#include "ck_dog_steer.h"

/* ── AXI GPIO Base Addresses (from block design) ── */
/* These map to the AXI GPIO IP blocks in the Vivado block design */
#define GPIO_HB_RD_ID      XPAR_AXI_GPIO_HB_RD_0_DEVICE_ID
#define GPIO_HB_WR_ID      XPAR_AXI_GPIO_HB_WR_0_DEVICE_ID
#define GPIO_GAIT_RD_ID    XPAR_AXI_GPIO_GAIT_RD_0_DEVICE_ID
#define GPIO_GAIT_WR_ID    XPAR_AXI_GPIO_GAIT_WR_0_DEVICE_ID
#define GPIO_SERVO_ID       XPAR_AXI_GPIO_SERVO_0_DEVICE_ID
#define GPIO_SERVO_CAL_ID   XPAR_AXI_GPIO_SERVO_CAL_0_DEVICE_ID
#define GPIO_LED_ID         XPAR_AXI_GPIO_LED_0_DEVICE_ID
#define GPIO_I2C_ID         XPAR_AXI_GPIO_I2C_0_DEVICE_ID
#define GPIO_MIC_ID         XPAR_AXI_GPIO_MIC_0_DEVICE_ID
#define GPIO_DAC_ID         XPAR_AXI_GPIO_DAC_0_DEVICE_ID

/* ── Shared Memory (OCM) ── */
#define OCM_BASE            0xFFFF0000
#define OCM_COHERENCE       (OCM_BASE + 0x00)  /* float: current coherence */
#define OCM_PHASE_BC        (OCM_BASE + 0x04)  /* uint8: heartbeat phase */
#define OCM_FUSE_OP         (OCM_BASE + 0x05)  /* uint8: fused operator */
#define OCM_BTQ_BAND        (OCM_BASE + 0x06)  /* uint8: 0=GREEN,1=YELLOW,2=RED */
#define OCM_STEER_MODE      (OCM_BASE + 0x07)  /* uint8: current steer mode */
#define OCM_GAIT_PHASE      (OCM_BASE + 0x08)  /* uint8: gait cycle phase */
#define OCM_TICK_COUNT       (OCM_BASE + 0x0C)  /* uint32: heartbeat tick count */
#define OCM_SERVO_OUT_BASE   (OCM_BASE + 0x10)  /* 12x uint16: servo targets */
#define OCM_SERVO_OBS_BASE   (OCM_BASE + 0x30)  /* 12x uint16: observed positions */
#define OCM_IMU_BASE         (OCM_BASE + 0x60)  /* 6x int16: accel + gyro */
#define OCM_READY            (OCM_BASE + 0x70)  /* uint32: Core 0 ready flag */

/* ── GPIO Instances ── */
static XGpio gpio_hb_rd, gpio_hb_wr;
static XGpio gpio_gait_rd, gpio_gait_wr;
static XGpio gpio_servo, gpio_servo_cal;
static XGpio gpio_led, gpio_i2c;

/* ── Dog Steering State ── */
static CK_DogSteer steer;

/* ── T* = 5/7 ── */
#define T_STAR_NUM  5
#define T_STAR_DEN  7

/* ── Read PL Heartbeat State via AXI GPIO ── */
static void read_heartbeat(uint32_t *tick_count, uint8_t *phase_bc,
                            uint8_t *fuse_op, uint16_t *coh_num,
                            uint16_t *coh_den, uint8_t *bump)
{
    /* Channel 1: {tick_count[31:0]} */
    uint32_t ch1 = XGpio_DiscreteRead(&gpio_hb_rd, 1);
    *tick_count = ch1;

    /* Channel 2: {coh_den[15:0], coh_num[15:0]} or packed fields */
    uint32_t ch2 = XGpio_DiscreteRead(&gpio_hb_rd, 2);
    *phase_bc = (ch2 >> 0) & 0xF;
    *fuse_op  = (ch2 >> 4) & 0xF;
    *bump     = (ch2 >> 8) & 0x1;
    *coh_num  = (ch2 >> 16) & 0xFFFF;

    /* Read coherence denominator from separate register or use packed */
    /* For now, read from write-back GPIO */
    *coh_den  = 32;  /* HISTORY parameter from heartbeat */
}

/* ── Read PL Gait Vortex State ── */
static void read_gait(uint16_t *vortex_flat, uint8_t *aligned_flat,
                       uint16_t *delta_flat, uint16_t *correction_flat,
                       uint8_t *gait_phase, uint8_t *all_aligned)
{
    uint32_t ch1 = XGpio_DiscreteRead(&gpio_gait_rd, 1);
    uint32_t ch2 = XGpio_DiscreteRead(&gpio_gait_rd, 2);

    *vortex_flat     = ch1 & 0xFFFF;
    *aligned_flat    = (ch1 >> 16) & 0xF;
    *all_aligned     = (ch1 >> 20) & 0x1;
    *gait_phase      = (ch1 >> 24) & 0xF;
    *delta_flat      = ch2 & 0xFFFF;
    *correction_flat = (ch2 >> 16) & 0xFFFF;
}

/* ── Write Gait Mode to PL ── */
static void write_gait_mode(uint8_t mode)
{
    XGpio_DiscreteWrite(&gpio_gait_wr, 1, mode & 0x3);
}

/* ── LED Control ── */
static void set_leds(uint8_t pattern)
{
    XGpio_DiscreteWrite(&gpio_led, 1, pattern);
}

/* ── Compute Coherence as Float ── */
static float compute_coherence(uint16_t num, uint16_t den)
{
    if (den == 0) return 0.0f;
    return (float)num / (float)den;
}

/* ── Core 0: Brain Loop (50 Hz) ── */
void core0_brain_loop(void)
{
    uint32_t tick_count;
    uint8_t  phase_bc, fuse_op, bump;
    uint16_t coh_num, coh_den;

    xil_printf("\r\n");
    xil_printf("========================================\r\n");
    xil_printf("  CK DOG BRAIN -- Core 0\r\n");
    xil_printf("  T* = 5/7 = 0.714285...\r\n");
    xil_printf("  Heartbeat is sovereign.\r\n");
    xil_printf("========================================\r\n");

    /* Signal Core 1 that we're ready */
    volatile uint32_t *ready = (volatile uint32_t *)OCM_READY;
    *ready = 0xCB5A5A;  /* Magic number: CK ready */

    uint32_t loop_count = 0;

    while (1) {
        /* Read heartbeat from PL */
        read_heartbeat(&tick_count, &phase_bc, &fuse_op,
                       &coh_num, &coh_den, &bump);

        float coherence = compute_coherence(coh_num, coh_den);

        /* Determine BTQ band */
        uint8_t band;
        if (coh_num * T_STAR_DEN >= coh_den * T_STAR_NUM)
            band = 0;  /* GREEN: coherent */
        else if (coherence >= 0.4f)
            band = 1;  /* YELLOW: blending */
        else
            band = 2;  /* RED: observing */

        /* Write to shared memory for Core 1 */
        volatile float    *ocm_coh   = (volatile float *)OCM_COHERENCE;
        volatile uint8_t  *ocm_phase = (volatile uint8_t *)OCM_PHASE_BC;
        volatile uint8_t  *ocm_fuse  = (volatile uint8_t *)OCM_FUSE_OP;
        volatile uint8_t  *ocm_band  = (volatile uint8_t *)OCM_BTQ_BAND;
        volatile uint32_t *ocm_tick  = (volatile uint32_t *)OCM_TICK_COUNT;

        *ocm_coh   = coherence;
        *ocm_phase = phase_bc;
        *ocm_fuse  = fuse_op;
        *ocm_band  = band;
        *ocm_tick  = tick_count;

        /* LED feedback */
        uint8_t led_pattern = 0;
        if (bump) led_pattern |= 0x1;        /* LED0: bump detected */
        if (band == 0) led_pattern |= 0x2;   /* LED1: GREEN band */
        set_leds(led_pattern);

        /* Status report every 5 seconds (250 ticks at 50 Hz) */
        if (loop_count % 250 == 0) {
            xil_printf("[CK] tick=%lu C=%d/%d=%d%% op=%d fuse=%d band=%s\r\n",
                       tick_count, coh_num, coh_den,
                       (int)(coherence * 100.0f),
                       phase_bc, fuse_op,
                       band == 0 ? "GREEN" : (band == 1 ? "YELLOW" : "RED"));
        }

        loop_count++;
        usleep(20000);  /* 50 Hz = 20ms */
    }
}

/* ── Core 1: Body Loop (50 Hz) ── */
void core1_body_loop(void)
{
    /* Wait for Core 0 to initialize */
    volatile uint32_t *ready = (volatile uint32_t *)OCM_READY;
    while (*ready != 0xCB5A5A) {
        usleep(1000);
    }

    xil_printf("[BODY] Core 1 starting -- dog body control\r\n");

    /* Initialize steering engine */
    ck_dog_steer_init(&steer);

    uint16_t vortex_flat, delta_flat, correction_flat;
    uint8_t  aligned_flat, gait_phase, all_aligned;

    while (1) {
        /* Read coherence from shared memory */
        volatile float   *ocm_coh  = (volatile float *)OCM_COHERENCE;
        volatile uint8_t *ocm_band = (volatile uint8_t *)OCM_BTQ_BAND;

        float coherence = *ocm_coh;
        uint8_t band = *ocm_band;

        /* Update steering engine coherence */
        ck_dog_steer_set_coherence(&steer, coherence, band);

        /* Read gait vortex from PL */
        read_gait(&vortex_flat, &aligned_flat, &delta_flat,
                  &correction_flat, &gait_phase, &all_aligned);

        /* Extract per-leg correction operators */
        for (int leg = 0; leg < 4; leg++) {
            uint8_t correction_op = (correction_flat >> (leg * 4)) & 0xF;

            /* Use servo_cal lookup to convert operator -> PWM angles */
            /* 3 joints per leg: hip, knee, ankle */
            /* For now, center all servos (BALANCE = 1500us) */
            uint16_t hip_us   = 1500;
            uint16_t knee_us  = 1500;
            uint16_t ankle_us = 1500;

            /* TODO: Read from servo_cal AXI GPIO or compute inline */
            /* The servo_cal.v module in PL does this lookup */

            ck_dog_steer_set_target(&steer, leg * 3 + 0, hip_us);
            ck_dog_steer_set_target(&steer, leg * 3 + 1, knee_us);
            ck_dog_steer_set_target(&steer, leg * 3 + 2, ankle_us);
        }

        /* Run steering tick */
        uint8_t mode = ck_dog_steer_tick(&steer);

        /* Write steer mode to shared memory */
        volatile uint8_t *ocm_mode = (volatile uint8_t *)OCM_STEER_MODE;
        *ocm_mode = mode;

        /* Write servo outputs to shared memory (for monitoring) */
        volatile uint16_t *ocm_servo = (volatile uint16_t *)OCM_SERVO_OUT_BASE;
        for (int i = 0; i < 12; i++) {
            ocm_servo[i] = ck_dog_steer_get_output(&steer, i);
        }

        /* Write gait phase */
        volatile uint8_t *ocm_gait = (volatile uint8_t *)OCM_GAIT_PHASE;
        *ocm_gait = gait_phase;

        usleep(20000);  /* 50 Hz */
    }
}

/* ── Main Entry Point ── */
int main(void)
{
    int status;

    xil_printf("\r\n");
    xil_printf("============================================\r\n");
    xil_printf("  CK DOG -- Coherence Keeper in Silicon\r\n");
    xil_printf("  (c) 2026 Brayden Sanders / 7Site LLC\r\n");
    xil_printf("  Trinity Infinity Geometry\r\n");
    xil_printf("============================================\r\n");
    xil_printf("  T* = 5/7.  He earns control.\r\n");
    xil_printf("============================================\r\n");

    /* Initialize AXI GPIO instances */
    status = XGpio_Initialize(&gpio_hb_rd, GPIO_HB_RD_ID);
    if (status != XST_SUCCESS) {
        xil_printf("[ERR] Heartbeat GPIO init failed\r\n");
        return -1;
    }
    XGpio_SetDataDirection(&gpio_hb_rd, 1, 0xFFFFFFFF);  /* All input */
    XGpio_SetDataDirection(&gpio_hb_rd, 2, 0xFFFFFFFF);

    status = XGpio_Initialize(&gpio_gait_rd, GPIO_GAIT_RD_ID);
    if (status != XST_SUCCESS) {
        xil_printf("[ERR] Gait GPIO init failed\r\n");
        return -1;
    }
    XGpio_SetDataDirection(&gpio_gait_rd, 1, 0xFFFFFFFF);
    XGpio_SetDataDirection(&gpio_gait_rd, 2, 0xFFFFFFFF);

    status = XGpio_Initialize(&gpio_gait_wr, GPIO_GAIT_WR_ID);
    if (status != XST_SUCCESS) {
        xil_printf("[ERR] Gait WR GPIO init failed\r\n");
        return -1;
    }
    XGpio_SetDataDirection(&gpio_gait_wr, 1, 0x00000000);  /* All output */

    status = XGpio_Initialize(&gpio_led, GPIO_LED_ID);
    if (status != XST_SUCCESS) {
        xil_printf("[ERR] LED GPIO init failed\r\n");
        return -1;
    }
    XGpio_SetDataDirection(&gpio_led, 1, 0x00000000);

    xil_printf("[INIT] All GPIO initialized\r\n");
    xil_printf("[INIT] Starting brain loop on Core 0...\r\n");

    /* For single-core bare-metal, run brain + body in same loop */
    /* For dual-core, Core 1 would be launched separately */
    /* TODO: Add Core 1 launch via OCM handshake */

    /* For now: single-core mode -- brain reads, observes, learns */
    core0_brain_loop();

    return 0;
}
