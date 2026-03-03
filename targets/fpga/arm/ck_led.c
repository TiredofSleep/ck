/*
 * ck_led.c -- LED Driver for CK Coherence Machine
 * ==================================================
 * Operator: BREATH (8) -- the LED breathes with CK.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

#include "ck_led.h"
#include "ck_brain.h"  /* for REG_WR/RD macros */
#include <math.h>

/* Operator color lookup table */
static const CK_Color OP_COLORS[10] = {
    CK_COLOR_VOID,
    CK_COLOR_LATTICE,
    CK_COLOR_COUNTER,
    CK_COLOR_PROGRESS,
    CK_COLOR_COLLAPSE,
    CK_COLOR_BALANCE,
    CK_COLOR_CHAOS,
    CK_COLOR_HARMONY,
    CK_COLOR_BREATH,
    CK_COLOR_RESET,
};

void ck_led_init(void) {
    /* Set LED GPIO pins as output (tri-state register: 0 = output) */
    REG_WR(CK_LED_GPIO_TRI, 0x00000000);
    /* Start dark */
    REG_WR(CK_LED_GPIO_DATA, 0x00000000);
}

CK_Color ck_led_op_color(uint8_t op) {
    if (op >= 10) return CK_COLOR_VOID;
    return OP_COLORS[op];
}

void ck_led_set_color(CK_Color color) {
    /*
     * Hardware mapping depends on Puzhi board LED config.
     * Common: 4 discrete LEDs on GPIO bits [3:0].
     * If RGB LED: use PWM via FPGA led_driver.v (Phase 2+).
     *
     * For now: use intensity (brightness) mapped to 4 LEDs.
     * Bit 0 = dim, Bit 1 = medium, Bit 2 = bright, Bit 3 = max.
     *
     * Extract perceived brightness: 0.299R + 0.587G + 0.114B
     */
    uint8_t r = (color >> 16) & 0xFF;
    uint8_t g = (color >> 8) & 0xFF;
    uint8_t b = color & 0xFF;
    uint32_t brightness = (299 * r + 587 * g + 114 * b) / 1000;

    /* Map brightness (0-255) to 4-bit LED pattern */
    uint32_t pattern = 0;
    if (brightness > 192) pattern = 0xF;       /* All 4 LEDs */
    else if (brightness > 128) pattern = 0x7;  /* 3 LEDs */
    else if (brightness > 64) pattern = 0x3;   /* 2 LEDs */
    else if (brightness > 16) pattern = 0x1;   /* 1 LED */
    /* else: all off */

    REG_WR(CK_LED_GPIO_DATA, pattern);
}

void ck_led_set_operator(uint8_t op) {
    ck_led_set_color(ck_led_op_color(op));
}

void ck_led_breathe(uint8_t op, float breath_phase) {
    /*
     * Modulate LED brightness by breath cycle.
     * breath_phase: 0.0 = start of INHALE, 1.0 = end of cycle
     * Brightness follows a sine curve:
     *   peak at EXHALE start (0.5), dim at INHALE start (0.0)
     */
    float intensity = 0.3f + 0.7f * sinf(breath_phase * 3.14159265f);
    if (intensity < 0.0f) intensity = 0.0f;
    if (intensity > 1.0f) intensity = 1.0f;

    CK_Color base = ck_led_op_color(op);
    uint8_t r = (uint8_t)(((base >> 16) & 0xFF) * intensity);
    uint8_t g = (uint8_t)(((base >> 8) & 0xFF) * intensity);
    uint8_t b = (uint8_t)((base & 0xFF) * intensity);

    ck_led_set_color(CK_RGB(r, g, b));
}

void ck_led_flash(CK_Color color, uint32_t duration_ms) {
    /*
     * Brief flash. Uses busy-wait since we're bare metal.
     * duration_ms is approximate (depends on CPU clock).
     */
    ck_led_set_color(color);

    /* Rough busy-wait: ~667 cycles per microsecond at 667MHz */
    volatile uint32_t count = duration_ms * 667000;
    while (count > 0) count--;

    ck_led_set_color(CK_COLOR_VOID);
}
