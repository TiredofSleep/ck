/*
 * ck_uart.c -- CK Serial Protocol on ARM (Bare Metal)
 * =====================================================
 * Operator: BALANCE (5) -- the bridge between bodies.
 *
 * Implements CK binary packet protocol over Zynq PS UART.
 * Compatible with ck_serial.py on the host side.
 *
 * Packet: [SYNC 'CK'] [TYPE 1B] [LEN 2B LE] [PAYLOAD] [CRC8]
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

#include "ck_uart.h"
#include "ck_brain.h"
#include <string.h>

/* ── CRC-8/MAXIM (same polynomial as ck_serial.py, ck_sd.c) ── */

uint8_t ck_uart_crc8(const uint8_t* data, uint16_t len) {
    uint8_t crc = 0x00;
    for (uint16_t i = 0; i < len; i++) {
        crc ^= data[i];
        for (int bit = 0; bit < 8; bit++) {
            if (crc & 0x80)
                crc = (crc << 1) ^ 0x31;
            else
                crc = crc << 1;
        }
    }
    return crc;
}

/* ── Low-level UART I/O ── */

static void uart_write_byte(uint8_t byte) {
    /* Wait until TX FIFO is not full */
    while (REG_RD(CK_UART_SR) & CK_UART_SR_TXFULL);
    REG_WR(CK_UART_FIFO, (uint32_t)byte);
}

static bool uart_read_byte(uint8_t* byte) {
    /* Check if RX FIFO has data */
    if (REG_RD(CK_UART_SR) & CK_UART_SR_RXEMPTY) {
        return false;
    }
    *byte = (uint8_t)(REG_RD(CK_UART_FIFO) & 0xFF);
    return true;
}

static void uart_write_buf(const uint8_t* buf, uint16_t len) {
    for (uint16_t i = 0; i < len; i++) {
        uart_write_byte(buf[i]);
    }
}

/* ── Serialization Helpers ── */

static void pack_u8(uint8_t* buf, uint16_t* pos, uint8_t val) {
    buf[(*pos)++] = val;
}

static void pack_u16_le(uint8_t* buf, uint16_t* pos, uint16_t val) {
    buf[(*pos)++] = val & 0xFF;
    buf[(*pos)++] = (val >> 8) & 0xFF;
}

static void pack_u32_le(uint8_t* buf, uint16_t* pos, uint32_t val) {
    buf[(*pos)++] = val & 0xFF;
    buf[(*pos)++] = (val >> 8) & 0xFF;
    buf[(*pos)++] = (val >> 16) & 0xFF;
    buf[(*pos)++] = (val >> 24) & 0xFF;
}

static void pack_f32_le(uint8_t* buf, uint16_t* pos, float val) {
    uint32_t* p = (uint32_t*)&val;
    pack_u32_le(buf, pos, *p);
}

/* ── Init ── */

void ck_uart_init(CK_UartState* uart) {
    memset(uart, 0, sizeof(CK_UartState));

    /*
     * Configure Zynq PS UART1 for 115200 baud, 8N1.
     *
     * The PS UART clock is typically 100MHz (from IO PLL).
     * Baud rate = UART_REF_CLK / (CD * (BDIV + 1))
     *
     * For 115200 baud with 100MHz clock:
     *   CD = 62, BDIV = 13 → 100e6 / (62 * 14) = 115207 ≈ 115200
     *
     * In a real Vitis project, xuartps.h handles this.
     * For bare metal, we configure registers directly.
     */

    /* Reset and disable UART */
    REG_WR(CK_UART_CR, 0x00000028);  /* TX_DIS | RX_DIS */

    /* Set baud rate: CD=62, BDIV=13 */
    REG_WR(CK_UART_BAUD_GEN, 62);
    REG_WR(CK_UART_BAUD_DIV, 13);

    /* Mode: 8 data bits, no parity, 1 stop bit, normal mode */
    REG_WR(CK_UART_MR, 0x00000020);

    /* Enable TX and RX */
    REG_WR(CK_UART_CR, 0x00000014);  /* TX_EN | RX_EN */

    uart->rx_state = 0;
}

/* ── Send Packet ── */

void ck_uart_send(CK_UartState* uart, uint8_t type,
                  const uint8_t* payload, uint16_t len) {
    /*
     * Build and send: [SYNC 'C''K'] [TYPE] [LEN LE] [PAYLOAD] [CRC8]
     * CRC covers everything from SYNC through end of PAYLOAD.
     */
    uint8_t header[CK_UART_HEADER_SIZE];
    uint16_t pos = 0;

    /* Header */
    header[pos++] = CK_UART_SYNC_0;  /* 'C' */
    header[pos++] = CK_UART_SYNC_1;  /* 'K' */
    header[pos++] = type;
    header[pos++] = len & 0xFF;
    header[pos++] = (len >> 8) & 0xFF;

    /* Compute CRC over header + payload */
    uint8_t crc = 0x00;
    for (uint16_t i = 0; i < CK_UART_HEADER_SIZE; i++) {
        crc ^= header[i];
        for (int bit = 0; bit < 8; bit++) {
            if (crc & 0x80) crc = (crc << 1) ^ 0x31;
            else crc = crc << 1;
        }
    }
    for (uint16_t i = 0; i < len; i++) {
        crc ^= payload[i];
        for (int bit = 0; bit < 8; bit++) {
            if (crc & 0x80) crc = (crc << 1) ^ 0x31;
            else crc = crc << 1;
        }
    }

    /* Transmit */
    uart_write_buf(header, CK_UART_HEADER_SIZE);
    if (len > 0 && payload != NULL) {
        uart_write_buf(payload, len);
    }
    uart_write_byte(crc);

    uart->tx_count++;
}

/* ── Send State Packet (0x81) ── */

void ck_uart_send_state(CK_UartState* uart,
                        uint8_t phase_b, uint8_t phase_d, uint8_t phase_bc,
                        uint8_t fuse_op, bool bump,
                        uint32_t tick_count, uint16_t coh_num, uint16_t coh_den,
                        uint32_t brain_ticks, uint8_t mode, uint8_t domain_count) {
    /*
     * STATE payload (20 bytes):
     *   [0]    phase_b
     *   [1]    phase_d
     *   [2]    phase_bc
     *   [3]    fuse_op
     *   [4]    bump (0/1)
     *   [5-8]  tick_count (u32 LE)
     *   [9-10] coh_num (u16 LE)
     *   [11-12] coh_den (u16 LE)
     *   [13-16] brain_ticks (u32 LE)
     *   [17]   mode
     *   [18]   domain_count
     *   [19]   reserved (0)
     */
    uint8_t payload[20];
    uint16_t pos = 0;

    pack_u8(payload, &pos, phase_b);
    pack_u8(payload, &pos, phase_d);
    pack_u8(payload, &pos, phase_bc);
    pack_u8(payload, &pos, fuse_op);
    pack_u8(payload, &pos, bump ? 1 : 0);
    pack_u32_le(payload, &pos, tick_count);
    pack_u16_le(payload, &pos, coh_num);
    pack_u16_le(payload, &pos, coh_den);
    pack_u32_le(payload, &pos, brain_ticks);
    pack_u8(payload, &pos, mode);
    pack_u8(payload, &pos, domain_count);
    pack_u8(payload, &pos, 0);  /* reserved */

    ck_uart_send(uart, CK_PKT_STATE, payload, 20);
}

/* ── Send Pong (0x86) ── */

void ck_uart_send_pong(CK_UartState* uart, const uint8_t* ping_payload, uint16_t len) {
    /* Echo back the ping payload (contains host timestamp) */
    ck_uart_send(uart, CK_PKT_PONG, ping_payload, len);
}

/* ── Send Crystal (0x83) ── */

void ck_uart_send_crystal(CK_UartState* uart,
                          const uint8_t* ops, uint8_t len,
                          uint8_t fuse, float confidence, uint32_t seen) {
    /*
     * CRYSTAL payload:
     *   [0]       pattern_len
     *   [1..len]  pattern ops
     *   [len+1]   fuse operator
     *   [len+2..5] confidence (f32 LE)
     *   [len+6..9] seen count (u32 LE)
     */
    uint8_t payload[CK_UART_MAX_PAYLOAD];
    uint16_t pos = 0;

    pack_u8(payload, &pos, len);
    for (uint8_t i = 0; i < len; i++) {
        pack_u8(payload, &pos, ops[i]);
    }
    pack_u8(payload, &pos, fuse);
    pack_f32_le(payload, &pos, confidence);
    pack_u32_le(payload, &pos, seen);

    ck_uart_send(uart, CK_PKT_CRYSTAL, payload, pos);
}

/* ── Poll for Received Packets ── */

bool ck_uart_poll(CK_UartState* uart) {
    /*
     * Non-blocking state machine parser.
     * Call this frequently. Returns true when a complete packet is ready.
     *
     * States:
     *   0: waiting for sync byte 0 ('C')
     *   1: waiting for sync byte 1 ('K')
     *   2: reading type
     *   3: reading len byte 0
     *   4: reading len byte 1
     *   5: reading payload bytes
     *   6: reading CRC
     */
    uint8_t byte;
    while (uart_read_byte(&byte)) {
        switch (uart->rx_state) {
            case 0: /* Sync byte 0 */
                if (byte == CK_UART_SYNC_0) {
                    uart->rx_buf[0] = byte;
                    uart->rx_pos = 1;
                    uart->rx_state = 1;
                }
                break;

            case 1: /* Sync byte 1 */
                if (byte == CK_UART_SYNC_1) {
                    uart->rx_buf[1] = byte;
                    uart->rx_pos = 2;
                    uart->rx_state = 2;
                } else {
                    uart->rx_state = 0;  /* Reset */
                }
                break;

            case 2: /* Type */
                uart->rx_type = byte;
                uart->rx_buf[2] = byte;
                uart->rx_pos = 3;
                uart->rx_state = 3;
                break;

            case 3: /* Length byte 0 (low) */
                uart->rx_len = byte;
                uart->rx_buf[3] = byte;
                uart->rx_pos = 4;
                uart->rx_state = 4;
                break;

            case 4: /* Length byte 1 (high) */
                uart->rx_len |= ((uint16_t)byte << 8);
                uart->rx_buf[4] = byte;
                uart->rx_pos = 5;
                uart->rx_payload_pos = 0;

                if (uart->rx_len > CK_UART_MAX_PAYLOAD) {
                    uart->rx_state = 0;  /* Too long, reset */
                } else if (uart->rx_len == 0) {
                    uart->rx_state = 6;  /* No payload, go to CRC */
                } else {
                    uart->rx_state = 5;  /* Read payload */
                }
                break;

            case 5: /* Payload bytes */
                uart->rx_buf[uart->rx_pos++] = byte;
                uart->rx_payload_pos++;
                if (uart->rx_payload_pos >= uart->rx_len) {
                    uart->rx_state = 6;
                }
                break;

            case 6: /* CRC */
            {
                uint16_t data_len = CK_UART_HEADER_SIZE + uart->rx_len;
                uint8_t computed_crc = ck_uart_crc8(uart->rx_buf, data_len);

                if (byte == computed_crc) {
                    /* Valid packet! */
                    uart->last_packet.type = uart->rx_type;
                    uart->last_packet.length = uart->rx_len;
                    if (uart->rx_len > 0) {
                        memcpy(uart->last_packet.payload,
                               uart->rx_buf + CK_UART_HEADER_SIZE,
                               uart->rx_len);
                    }
                    uart->last_packet.valid = true;
                    uart->rx_count++;
                    uart->rx_state = 0;
                    return true;
                } else {
                    /* CRC mismatch */
                    uart->crc_errors++;
                    uart->rx_state = 0;
                }
                break;
            }
        }
    }
    return false;
}

/* ── Get Last Packet ── */

CK_Packet* ck_uart_get_packet(CK_UartState* uart) {
    if (uart->last_packet.valid) {
        return &uart->last_packet;
    }
    return NULL;
}
