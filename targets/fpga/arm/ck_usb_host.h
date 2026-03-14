/*
 * ck_usb_host.h -- USB Host Serial Driver for Dog Connection
 * ============================================================
 * Operator: BALANCE (5) -- the bridge between CK's brain and the dog's body.
 *
 * Drives the PS USB 2.0 Host controller (via USB3320 ULPI PHY)
 * to communicate with the XiaoR dog's controller board over USB-C.
 *
 * The dog's USB-C presents a USB CDC serial device (virtual COM port).
 * CK enumerates it, opens the serial port, and sends/receives
 * LewanSoul servo protocol packets.
 *
 * This uses the Xilinx USB standalone driver (xusbps).
 * The driver handles:
 *   1. USB host initialization + PHY setup
 *   2. Device enumeration (find CDC serial device)
 *   3. Bulk IN/OUT transfers for serial data
 *   4. Simple TX/RX ring buffers for packet framing
 *
 * Usage from ck_core1.c:
 *   ck_usb_host_init(&usb);
 *   // In body loop:
 *   ck_usb_host_poll(&usb);  // Process USB events
 *   ck_usb_host_tx(&usb, data, len);  // Send to dog
 *   int n = ck_usb_host_rx(&usb, buf, max);  // Read from dog
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

#ifndef CK_USB_HOST_H
#define CK_USB_HOST_H

#include <stdint.h>
#include <stdbool.h>

/* ── USB Host State ── */

#define CK_USB_TX_BUF_SIZE  512
#define CK_USB_RX_BUF_SIZE  512

typedef struct {
    /* Connection state */
    bool     initialized;      /* USB controller initialized */
    bool     device_connected; /* CDC device enumerated and ready */
    uint8_t  device_addr;      /* USB device address */
    uint8_t  bulk_in_ep;       /* Bulk IN endpoint (dog -> CK) */
    uint8_t  bulk_out_ep;      /* Bulk OUT endpoint (CK -> dog) */

    /* TX ring buffer */
    uint8_t  tx_buf[CK_USB_TX_BUF_SIZE];
    uint16_t tx_head;
    uint16_t tx_tail;

    /* RX ring buffer */
    uint8_t  rx_buf[CK_USB_RX_BUF_SIZE];
    uint16_t rx_head;
    uint16_t rx_tail;

    /* Stats */
    uint32_t tx_bytes;
    uint32_t rx_bytes;
    uint32_t errors;
    uint32_t resets;
} CK_UsbHost;

/* ── Zynq PS USB Controller ── */

/* PS USB0 base address (used as Host) */
#define CK_USB_BASE           0xE0002000

/* USB controller registers */
#define CK_USB_CMD            (CK_USB_BASE + 0x140)  /* USB command */
#define CK_USB_STS            (CK_USB_BASE + 0x144)  /* USB status */
#define CK_USB_INTR           (CK_USB_BASE + 0x148)  /* USB interrupt enable */
#define CK_USB_PORTSC         (CK_USB_BASE + 0x184)  /* Port status/control */
#define CK_USB_MODE           (CK_USB_BASE + 0x1A8)  /* USB mode */
#define CK_USB_PERIODICBASE   (CK_USB_BASE + 0x154)  /* Periodic frame list */
#define CK_USB_ASYNCBASE      (CK_USB_BASE + 0x158)  /* Async list address */

/* USB mode bits */
#define CK_USB_MODE_HOST      0x03   /* Host mode */
#define CK_USB_CMD_RUN        (1 << 0)
#define CK_USB_CMD_RESET      (1 << 1)
#define CK_USB_PORTSC_CONN    (1 << 0)  /* Device connected */
#define CK_USB_PORTSC_PE      (1 << 2)  /* Port enabled */

/* ── Functions ── */

/* Initialize USB host controller and PHY */
void ck_usb_host_init(CK_UsbHost* usb);

/* Poll for USB events (call every body tick).
 * Handles enumeration, connection, data transfer.
 * Returns true if device is connected and ready. */
bool ck_usb_host_poll(CK_UsbHost* usb);

/* Send data to the dog (queued in TX buffer, sent on next poll) */
void ck_usb_host_tx(CK_UsbHost* usb, const uint8_t* data, uint16_t len);

/* Read data from the dog (from RX buffer, filled by poll).
 * Returns number of bytes read. */
uint16_t ck_usb_host_rx(CK_UsbHost* usb, uint8_t* buf, uint16_t max_len);

/* Send a LewanSoul servo command through USB to dog */
void ck_usb_servo_move(CK_UsbHost* usb, uint8_t id,
                        uint16_t angle, uint16_t time_ms);

/* Send e-stop to all servos through USB */
void ck_usb_servo_estop(CK_UsbHost* usb);

/* Request servo position readback (CMD 0x1C) */
void ck_usb_servo_read_pos(CK_UsbHost* usb, uint8_t id);

/* Check if USB connection to dog is active */
bool ck_usb_host_connected(CK_UsbHost* usb);

#endif /* CK_USB_HOST_H */
