/*
 * ck_led.h -- LED Driver for CK Coherence Machine
 * ==================================================
 * Operator: BREATH (8) -- the LED breathes with CK.
 *
 * Maps CK operators and body state to LED RGB patterns.
 * Hardware: Puzhi board onboard LEDs (directly GPIO-driven).
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

#ifndef CK_LED_H
#define CK_LED_H

#include <stdint.h>
#include <stdbool.h>

/* RGB color packed into 24 bits: [R:8][G:8][B:8] */
typedef uint32_t CK_Color;

#define CK_RGB(r,g,b) (((uint32_t)(r) << 16) | ((uint32_t)(g) << 8) | (uint32_t)(b))

/* Operator colors -- each operator has an identity color */
#define CK_COLOR_VOID      CK_RGB(  0,   0,   0)  /* Black / off */
#define CK_COLOR_LATTICE   CK_RGB(  0,  80, 255)  /* Structure blue */
#define CK_COLOR_COUNTER   CK_RGB(255, 255, 255)  /* Measuring white */
#define CK_COLOR_PROGRESS  CK_RGB(  0, 200,  60)  /* Growth green */
#define CK_COLOR_COLLAPSE  CK_RGB(255,  30,  10)  /* Danger red */
#define CK_COLOR_BALANCE   CK_RGB(255, 180,   0)  /* Tension amber */
#define CK_COLOR_CHAOS     CK_RGB(255,   0,  60)  /* Disruption hot red */
#define CK_COLOR_HARMONY   CK_RGB( 80, 200, 255)  /* Peace blue-cyan */
#define CK_COLOR_BREATH    CK_RGB(100, 100, 220)  /* Calm blue-purple */
#define CK_COLOR_RESET     CK_RGB(255, 255, 255)  /* Flash white */

/* Special state colors */
#define CK_COLOR_SOVEREIGN CK_RGB(255, 200,  50)  /* Gold -- coherence >= T* */
#define CK_COLOR_BUMP      CK_RGB(255, 255, 255)  /* White flash -- bump pair */

/* LED GPIO base address -- adjust for your specific Puzhi board */
#define CK_LED_GPIO_BASE   0x41200000  /* AXI GPIO IP base (Vivado-assigned) */
#define CK_LED_GPIO_DATA   (CK_LED_GPIO_BASE + 0x00)
#define CK_LED_GPIO_TRI    (CK_LED_GPIO_BASE + 0x04)

/* Initialize LED GPIO as output */
void ck_led_init(void);

/* Set LED to a specific color (hardware-dependent) */
void ck_led_set_color(CK_Color color);

/* Set LED from operator index (0-9) */
void ck_led_set_operator(uint8_t op);

/* Update LED with breath modulation (brightness follows sine curve) */
void ck_led_breathe(uint8_t op, float breath_phase);

/* Flash LED briefly (for bumps, events) */
void ck_led_flash(CK_Color color, uint32_t duration_ms);

/* Get the color for a given operator */
CK_Color ck_led_op_color(uint8_t op);

#endif /* CK_LED_H */
