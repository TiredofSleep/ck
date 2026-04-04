/*
 * ck_uart.h -- CK Serial Protocol on ARM (Bare Metal)
 * =====================================================
 * Operator: BALANCE (5) -- the bridge between bodies.
 *
 * Implements the CK binary packet protocol on the Zynq UART.
 * Same protocol as ck_serial.py (host side), but in C.
 *
 * Packet format:
 *   [SYNC 'C''K'] [TYPE 1B] [LEN 2B LE] [PAYLOAD] [CRC8 1B]
 *
 * This UART serves two purposes:
 *   1. Talk to Windows host (R16) during development
 *   2. Talk to dog body (ESP32) when attached
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

#ifndef CK_UART_H
#define CK_UART_H

#include <stdint.h>
#include <stdbool.h>

/* ── Packet Types ── */

/* Zybo → Host / Dog */
#define CK_PKT_STATE      0x81  /* Full heartbeat state */
#define CK_PKT_DECISION   0x82  /* Scheduling decision */
#define CK_PKT_CRYSTAL    0x83  /* New crystal formed */
#define CK_PKT_DOMAIN     0x84  /* Domain sovereignty change */
#define CK_PKT_TL_REQUEST 0x85  /* Request TL data */
#define CK_PKT_PONG       0x86  /* Heartbeat response */

/* Host / Dog → Zybo */
#define CK_PKT_OBSERVE    0x01  /* Process observation */
#define CK_PKT_SWARM      0x02  /* Swarm summary */
#define CK_PKT_DEEP_OBS   0x03  /* Deep kernel metrics */
#define CK_PKT_CONFIG     0x04  /* Configuration update */
#define CK_PKT_TL_CHUNK   0x05  /* TL data transfer */
#define CK_PKT_PING       0x06  /* Heartbeat check */

/* Dog-specific packet types (Phase 5+) */
#define CK_PKT_MOTOR      0x20  /* Motor command (op + intensity + btq) */
#define CK_PKT_LED_CMD    0x21  /* LED command (pattern + RGB) */
#define CK_PKT_SERVO      0x22  /* Servo command (ch + angle + speed) */
#define CK_PKT_GAIT       0x23  /* Gait frame (12 servo batch) */
#define CK_PKT_ESTOP      0x2E  /* Emergency stop */
#define CK_PKT_SENSOR     0xA0  /* Sensor report from dog */
#define CK_PKT_SERVO_POS  0xA1  /* Servo position feedback */
#define CK_PKT_PROXIMITY  0xA2  /* Ultrasonic + infrared data */

/* ── Constants ── */

#define CK_UART_MAX_PAYLOAD  256
#define CK_UART_SYNC_0       0x43  /* 'C' */
#define CK_UART_SYNC_1       0x4B  /* 'K' */
#define CK_UART_HEADER_SIZE  5     /* sync(2) + type(1) + len(2) */

/* ── Zynq UART Hardware ── */

/* PS UART1 (connected to USB-serial on most Zynq boards) */
#define CK_UART_BASE         0xE0001000
#define CK_UART_CR           (CK_UART_BASE + 0x00)  /* Control register */
#define CK_UART_MR           (CK_UART_BASE + 0x04)  /* Mode register */
#define CK_UART_SR           (CK_UART_BASE + 0x2C)  /* Status register */
#define CK_UART_FIFO         (CK_UART_BASE + 0x30)  /* TX/RX FIFO */
#define CK_UART_BAUD_DIV     (CK_UART_BASE + 0x34)  /* Baud rate divider */
#define CK_UART_BAUD_GEN     (CK_UART_BASE + 0x18)  /* Baud rate generator */

/* Status register bits */
#define CK_UART_SR_TXFULL    (1 << 4)
#define CK_UART_SR_TXEMPTY   (1 << 3)
#define CK_UART_SR_RXEMPTY   (1 << 1)

/* ── Received Packet ── */

typedef struct {
    uint8_t  type;
    uint16_t length;
    uint8_t  payload[CK_UART_MAX_PAYLOAD];
    bool     valid;
} CK_Packet;

/* ── UART State ── */

typedef struct {
    /* RX state machine */
    uint8_t  rx_buf[CK_UART_MAX_PAYLOAD + 10];
    uint16_t rx_pos;
    uint8_t  rx_state;  /* 0=sync0, 1=sync1, 2=type, 3=len0, 4=len1, 5=payload, 6=crc */
    uint8_t  rx_type;
    uint16_t rx_len;
    uint16_t rx_payload_pos;

    /* Last received packet */
    CK_Packet last_packet;

    /* Counters */
    uint32_t tx_count;
    uint32_t rx_count;
    uint32_t crc_errors;
} CK_UartState;

/* ── Functions ── */

/* Initialize UART hardware (115200 baud, 8N1) */
void ck_uart_init(CK_UartState* uart);

/* Send a raw packet */
void ck_uart_send(CK_UartState* uart, uint8_t type,
                  const uint8_t* payload, uint16_t len);

/* Send heartbeat state packet */
void ck_uart_send_state(CK_UartState* uart,
                        uint8_t phase_b, uint8_t phase_d, uint8_t phase_bc,
                        uint8_t fuse_op, bool bump,
                        uint32_t tick_count, uint16_t coh_num, uint16_t coh_den,
                        uint32_t brain_ticks, uint8_t mode, uint8_t domain_count);

/* Send pong (response to ping) */
void ck_uart_send_pong(CK_UartState* uart, const uint8_t* ping_payload, uint16_t len);

/* Send crystal notification */
void ck_uart_send_crystal(CK_UartState* uart,
                          const uint8_t* ops, uint8_t len,
                          uint8_t fuse, float confidence, uint32_t seen);

/* Poll for received packets (non-blocking). Returns true if packet available. */
bool ck_uart_poll(CK_UartState* uart);

/* Get the last received packet */
CK_Packet* ck_uart_get_packet(CK_UartState* uart);

/* CRC-8/MAXIM (same as ck_serial.py) */
uint8_t ck_uart_crc8(const uint8_t* data, uint16_t len);

#endif /* CK_UART_H */
