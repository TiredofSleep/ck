/*
 * ck_usb_host.c -- USB Host Serial Driver for Dog Connection
 * ============================================================
 * Operator: BALANCE (5) -- the bridge between CK and his body.
 *
 * The dog's USB-C goes to the FPGA's USB 2.0 Host port.
 * The dog's controller board appears as a USB CDC serial device.
 * CK talks LewanSoul protocol through this USB serial link.
 *
 * This is a minimal bare-metal USB host driver using the Zynq
 * PS EHCI controller directly. For full USB stack, use Xilinx
 * xusbps driver from the BSP. This simplified version handles
 * the common case: one CDC device, bulk transfers only.
 *
 * NOTE: Full USB enumeration + CDC class negotiation is complex.
 * This file provides the framework. The Xilinx BSP will handle
 * the low-level EHCI details when built with Vitis.
 *
 * If the dog's controller uses a simple FTDI/CH340/CP2102 USB-UART
 * chip (common in hobby robots), it may not even need CDC --
 * it might just be a vendor-class serial device. In that case,
 * the driver needs adjusted VID/PID matching.
 *
 * ALTERNATIVE (simpler): If the dog's USB-C connector has direct
 * UART lines (some robot dogs route TX/RX/GND through USB-C
 * without a USB stack), then bypass this entirely and wire
 * directly to PS UART or a free JM2 pin.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

#include "ck_usb_host.h"
#include "ck_brain.h"
#include <string.h>

/* ── Ring Buffer Helpers ── */

static uint16_t ring_count(uint16_t head, uint16_t tail, uint16_t size) {
    return (head - tail) & (size - 1);
}

static void ring_push(uint8_t* buf, uint16_t* head, uint16_t size,
                       uint8_t byte) {
    uint16_t next = (*head + 1) & (size - 1);
    buf[*head] = byte;
    *head = next;
}

static uint8_t ring_pop(uint8_t* buf, uint16_t* tail, uint16_t size) {
    uint8_t byte = buf[*tail];
    *tail = (*tail + 1) & (size - 1);
    return byte;
}

/* ── USB Host Init ── */

void ck_usb_host_init(CK_UsbHost* usb) {
    memset(usb, 0, sizeof(CK_UsbHost));

    /* Reset USB controller */
    REG_WR(CK_USB_CMD, CK_USB_CMD_RESET);

    /* Wait for reset complete */
    volatile int timeout = 10000;
    while ((REG_RD(CK_USB_CMD) & CK_USB_CMD_RESET) && timeout > 0)
        timeout--;

    /* Set host mode */
    REG_WR(CK_USB_MODE, CK_USB_MODE_HOST);

    /* Start controller */
    REG_WR(CK_USB_CMD, CK_USB_CMD_RUN);

    /* NOTE: Full EHCI initialization requires:
     * 1. Configure periodic frame list (for interrupt transfers)
     * 2. Configure async schedule (for control + bulk transfers)
     * 3. Enable port power
     * 4. Wait for device connection
     * 5. Reset port
     * 6. Enumerate device (GET_DESCRIPTOR, SET_ADDRESS, SET_CONFIG)
     * 7. Find CDC bulk IN/OUT endpoints
     * 8. Set line coding (115200 8N1)
     *
     * The Xilinx BSP (xusbps) handles all of this.
     * When building in Vitis, replace this init with:
     *   XUsbPs_Config *cfg = XUsbPs_LookupConfig(XPAR_XUSBPS_0_DEVICE_ID);
     *   XUsbPs_CfgInitialize(&usb_inst, cfg, cfg->BaseAddress);
     *   XUsbPs_SetMode(&usb_inst, XUSBPS_MODE_HOST);
     */

    usb->initialized = true;
}

/* ── USB Host Poll ── */

bool ck_usb_host_poll(CK_UsbHost* usb) {
    if (!usb->initialized) return false;

    /* Check if device is connected */
    uint32_t portsc = REG_RD(CK_USB_PORTSC);
    bool connected = (portsc & CK_USB_PORTSC_CONN) != 0;

    if (connected && !usb->device_connected) {
        /* New device connected -- need enumeration.
         * In Vitis BSP, this triggers the USB host stack
         * to enumerate and configure the CDC device.
         *
         * For now, mark as connected after a brief delay.
         * The actual enumeration will be handled by the BSP. */
        usb->device_connected = true;
        usb->device_addr = 1;  /* First device */
        usb->bulk_in_ep = 0x81;   /* Common CDC bulk IN */
        usb->bulk_out_ep = 0x02;  /* Common CDC bulk OUT */
    } else if (!connected && usb->device_connected) {
        /* Device disconnected */
        usb->device_connected = false;
        usb->resets++;
    }

    /* If connected, process TX buffer -> USB bulk OUT */
    if (usb->device_connected) {
        uint16_t tx_count = ring_count(usb->tx_head, usb->tx_tail,
                                        CK_USB_TX_BUF_SIZE);
        if (tx_count > 0) {
            /* In real implementation:
             * 1. Build a Transfer Descriptor (TD)
             * 2. Point it at tx_buf[tx_tail..tx_tail+count]
             * 3. Link TD into async schedule
             * 4. Wait for completion
             * 5. Advance tx_tail
             *
             * With Xilinx BSP:
             *   XUsbPs_EpBufferSend(&usb_inst, bulk_out_ep,
             *                        &tx_buf[tx_tail], tx_count);
             */
            usb->tx_bytes += tx_count;
            usb->tx_tail = usb->tx_head;  /* Mark as sent */
        }

        /* Process USB bulk IN -> RX buffer */
        /* In real implementation:
         * 1. Check if bulk IN TD completed
         * 2. Copy received data into rx_buf
         * 3. Advance rx_head
         *
         * With Xilinx BSP:
         *   uint32_t rx_len;
         *   XUsbPs_EpBufferReceive(&usb_inst, bulk_in_ep,
         *                           &rx_tmp, &rx_len);
         *   memcpy(&rx_buf[rx_head], rx_tmp, rx_len);
         */
    }

    return usb->device_connected;
}

/* ── TX / RX ── */

void ck_usb_host_tx(CK_UsbHost* usb, const uint8_t* data, uint16_t len) {
    for (uint16_t i = 0; i < len; i++) {
        ring_push(usb->tx_buf, &usb->tx_head, CK_USB_TX_BUF_SIZE, data[i]);
    }
}

uint16_t ck_usb_host_rx(CK_UsbHost* usb, uint8_t* buf, uint16_t max_len) {
    uint16_t count = ring_count(usb->rx_head, usb->rx_tail,
                                 CK_USB_RX_BUF_SIZE);
    if (count > max_len) count = max_len;
    for (uint16_t i = 0; i < count; i++) {
        buf[i] = ring_pop(usb->rx_buf, &usb->rx_tail, CK_USB_RX_BUF_SIZE);
    }
    return count;
}

bool ck_usb_host_connected(CK_UsbHost* usb) {
    return usb->device_connected;
}

/* ── LewanSoul Servo Commands via USB ── */

void ck_usb_servo_move(CK_UsbHost* usb, uint8_t id,
                        uint16_t angle, uint16_t time_ms) {
    if (!usb->device_connected) return;

    uint8_t pkt[10];
    pkt[0] = 0x55;
    pkt[1] = 0x55;
    pkt[2] = id;
    pkt[3] = 7;  /* SERVO_MOVE_LEN */
    pkt[4] = 1;  /* SERVO_CMD_MOVE */
    pkt[5] = angle & 0xFF;
    pkt[6] = (angle >> 8) & 0xFF;
    pkt[7] = time_ms & 0xFF;
    pkt[8] = (time_ms >> 8) & 0xFF;

    uint8_t sum = pkt[2] + pkt[3] + pkt[4] + pkt[5] + pkt[6] + pkt[7] + pkt[8];
    pkt[9] = ~sum;

    ck_usb_host_tx(usb, pkt, 10);
}

void ck_usb_servo_estop(CK_UsbHost* usb) {
    /* Center all 8 servos immediately */
    for (uint8_t id = 1; id <= 8; id++) {
        ck_usb_servo_move(usb, id, 500, 0);  /* 500 = center angle */
    }
}

void ck_usb_servo_read_pos(CK_UsbHost* usb, uint8_t id) {
    if (!usb->device_connected) return;

    /* LewanSoul CMD 28 (0x1C): SERVO_POS_READ */
    uint8_t pkt[6];
    pkt[0] = 0x55;
    pkt[1] = 0x55;
    pkt[2] = id;
    pkt[3] = 3;     /* Length */
    pkt[4] = 0x1C;  /* SERVO_POS_READ */

    uint8_t sum = pkt[2] + pkt[3] + pkt[4];
    pkt[5] = ~sum;

    ck_usb_host_tx(usb, pkt, 6);

    /* Response will come back on bulk IN:
     * [0x55][0x55][ID][5][0x1C][pos_lo][pos_hi][checksum]
     * Parse in ck_usb_host_poll() or in the body loop. */
}
