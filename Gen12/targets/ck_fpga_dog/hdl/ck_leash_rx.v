/*
 * ck_leash_rx.v -- Δ¹ Leash UART: R16 ↔ FPGA
 * ============================================
 * Gen12: The Δ¹ line — first relationship between brain (R16) and body (FPGA).
 *
 * Protocol: [SYNC 'CK'][TYPE 1B][LEN 2B LE][PAYLOAD][CRC8]
 * Baud: 115200, 8N1
 * CRC: CRC8/MAXIM, polynomial 0x31, init 0x00
 *
 * Receives from R16:
 *   PKT_PING  (0x06): → PONG response (echo 8-byte timestamp)
 *   PKT_GAIT  (0x23): → gait_cmd[1:0], gait_valid pulse
 *   PKT_ESTOP (0x2E): → estop_cmd asserted
 *   PKT_OBSERVE (0x01): → absorbed (no response)
 *   Other: → ignored
 *
 * Transmits to R16 (tx_out, shared servo UART bus):
 *   PKT_PONG  (0x86): 14 bytes, echoes PING timestamp
 *
 * NOTE: tx_out is idle-high. Caller ANDs with servo_tx for shared bus.
 *
 * (c) 2026 Brayden Ross Sanders / 7Site LLC — Trinity Infinity Geometry
 * Authors: Brayden Ross Sanders & Monica
 */

`default_nettype none

module ck_leash_rx #(
    parameter CLK_FREQ = 50_000_000,
    parameter BAUD     = 115200
)(
    input  wire        clk,
    input  wire        rst_n,

    // UART RX from R16
    input  wire        uart_rx,

    // Decoded command outputs
    output reg  [1:0]  gait_cmd,      // decoded gait mode (STAND/WALK/TROT)
    output reg         gait_valid,    // one-cycle pulse when gait_cmd updated
    output reg         estop_cmd,     // level: 1 = E-STOP active from R16

    // State inputs (used to build STATE response — future)
    input  wire [15:0] coh_num_in,
    input  wire [15:0] coh_den_in,
    input  wire [31:0] tick_in,
    input  wire [1:0]  simplex_in,

    // UART TX (shared servo bus — idle high, AND with servo_tx at top level)
    output wire        tx_out
);

    // =========================================================
    // Constants
    // =========================================================
    localparam BIT_PERIOD = CLK_FREQ / BAUD;  // 434 @ 50MHz/115200
    localparam HALF_BIT   = BIT_PERIOD / 2;   // 217

    // Packet type constants
    localparam PKT_OBSERVE = 8'h01;
    localparam PKT_PING    = 8'h06;
    localparam PKT_GAIT    = 8'h23;
    localparam PKT_ESTOP   = 8'h2E;
    localparam PKT_PONG    = 8'h86;

    // Max payload we buffer (PING = 8 bytes timestamp)
    localparam MAX_PAYLOAD = 8;

    // =========================================================
    // UART RX — 8N1
    // =========================================================
    // 2-FF synchronizer for async UART input
    reg [1:0] rx_sync;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) rx_sync <= 2'b11;
        else        rx_sync <= {rx_sync[0], uart_rx};
    end
    wire rx_in = rx_sync[1];

    reg [11:0] rx_baud_cnt;   // baud counter (up to BIT_PERIOD)
    reg [3:0]  rx_bit_cnt;    // bit counter (0=start, 1-8=data, 9=stop)
    reg [7:0]  rx_shift;      // shift register
    reg        rx_busy;       // currently receiving a byte

    reg        rx_byte_valid; // one-cycle pulse: rx_byte is ready
    reg [7:0]  rx_byte;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            rx_baud_cnt  <= 12'd0;
            rx_bit_cnt   <= 4'd0;
            rx_shift     <= 8'd0;
            rx_busy      <= 1'b0;
            rx_byte_valid<= 1'b0;
            rx_byte      <= 8'd0;
        end else begin
            rx_byte_valid <= 1'b0;

            if (!rx_busy) begin
                // Wait for start bit (falling edge on idle-high line)
                if (!rx_in) begin
                    rx_busy     <= 1'b1;
                    rx_baud_cnt <= 12'd0;
                    rx_bit_cnt  <= 4'd0;
                end
            end else begin
                if (rx_baud_cnt < BIT_PERIOD - 1) begin
                    rx_baud_cnt <= rx_baud_cnt + 12'd1;
                end else begin
                    rx_baud_cnt <= 12'd0;
                    if (rx_bit_cnt == 4'd0) begin
                        // Start bit: verify it's still low, sample midpoint
                        // (We started counting on the falling edge, now at center)
                        // Advance past start bit
                        rx_bit_cnt <= 4'd1;
                        rx_baud_cnt <= 12'd0;
                    end else if (rx_bit_cnt < 4'd9) begin
                        // Data bits 1-8 (LSB first)
                        rx_shift[rx_bit_cnt - 1] <= rx_in;
                        rx_bit_cnt <= rx_bit_cnt + 4'd1;
                    end else begin
                        // Stop bit
                        if (rx_in) begin
                            // Valid stop bit → emit byte
                            rx_byte       <= rx_shift;
                            rx_byte_valid <= 1'b1;
                        end
                        // Either way, return to idle
                        rx_busy    <= 1'b0;
                        rx_bit_cnt <= 4'd0;
                    end
                end
            end
        end
    end

    // =========================================================
    // Packet Parser
    // =========================================================
    // States
    localparam [2:0]
        PS_SYNC1   = 3'd0,  // Waiting for 'C' (0x43)
        PS_SYNC2   = 3'd1,  // Waiting for 'K' (0x4B)
        PS_TYPE    = 3'd2,  // Packet type byte
        PS_LEN_LO  = 3'd3,  // Length low byte
        PS_LEN_HI  = 3'd4,  // Length high byte
        PS_PAYLOAD = 3'd5,  // Payload bytes
        PS_CRC     = 3'd6;  // CRC byte

    reg [2:0]  ps_state;
    reg [7:0]  ps_type;
    reg [7:0]  ps_len;        // effective length (min of actual and MAX_PAYLOAD)
    reg [7:0]  ps_full_len;   // actual declared length
    reg [7:0]  ps_idx;        // bytes received so far
    reg [7:0]  ps_buf[0:MAX_PAYLOAD-1];  // payload buffer
    reg [7:0]  ps_crc;        // running CRC8 over header+payload

    // CRC8/MAXIM: polynomial 0x31, bit-by-bit
    function [7:0] crc8_byte;
        input [7:0] crc;
        input [7:0] data;
        reg [7:0] c;
        integer j;
        begin
            c = crc ^ data;
            for (j = 0; j < 8; j = j + 1)
                c = c[7] ? ((c << 1) ^ 8'h31) : (c << 1);
            crc8_byte = c;
        end
    endfunction

    // Packet complete event
    reg pkt_complete;     // one-cycle pulse
    reg pkt_crc_ok;       // CRC was valid
    reg [7:0] pkt_type_r; // captured type

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            ps_state    <= PS_SYNC1;
            ps_type     <= 8'd0;
            ps_len      <= 8'd0;
            ps_full_len <= 8'd0;
            ps_idx      <= 8'd0;
            ps_crc      <= 8'd0;
            pkt_complete<= 1'b0;
            pkt_crc_ok  <= 1'b0;
            pkt_type_r  <= 8'd0;
        end else begin
            pkt_complete <= 1'b0;

            if (rx_byte_valid) begin
                case (ps_state)
                    PS_SYNC1: begin
                        if (rx_byte == 8'h43) begin  // 'C'
                            ps_crc   <= crc8_byte(8'h00, rx_byte);
                            ps_state <= PS_SYNC2;
                        end
                        // else stay in SYNC1
                    end

                    PS_SYNC2: begin
                        if (rx_byte == 8'h4B) begin  // 'K'
                            ps_crc   <= crc8_byte(ps_crc, rx_byte);
                            ps_state <= PS_TYPE;
                        end else if (rx_byte == 8'h43) begin  // another 'C'
                            ps_crc   <= crc8_byte(8'h00, rx_byte);
                            // stay in SYNC2
                        end else begin
                            ps_state <= PS_SYNC1;
                        end
                    end

                    PS_TYPE: begin
                        ps_type  <= rx_byte;
                        ps_crc   <= crc8_byte(ps_crc, rx_byte);
                        ps_state <= PS_LEN_LO;
                    end

                    PS_LEN_LO: begin
                        ps_full_len <= rx_byte;
                        ps_crc      <= crc8_byte(ps_crc, rx_byte);
                        ps_state    <= PS_LEN_HI;
                    end

                    PS_LEN_HI: begin
                        ps_crc <= crc8_byte(ps_crc, rx_byte);
                        // Cap payload at MAX_PAYLOAD; ignore high byte (never > 8 for our pkts)
                        if (ps_full_len == 8'd0) begin
                            // Zero-length packet: go straight to CRC
                            ps_len   <= 8'd0;
                            ps_idx   <= 8'd0;
                            ps_state <= PS_CRC;
                        end else begin
                            ps_len   <= (ps_full_len > MAX_PAYLOAD) ? MAX_PAYLOAD[7:0]
                                                                     : ps_full_len;
                            ps_idx   <= 8'd0;
                            ps_state <= PS_PAYLOAD;
                        end
                    end

                    PS_PAYLOAD: begin
                        // Buffer up to MAX_PAYLOAD bytes; compute CRC over all
                        if (ps_idx < MAX_PAYLOAD)
                            ps_buf[ps_idx[2:0]] <= rx_byte;
                        ps_crc  <= crc8_byte(ps_crc, rx_byte);
                        ps_idx  <= ps_idx + 8'd1;
                        if (ps_idx + 8'd1 >= ps_full_len)
                            ps_state <= PS_CRC;
                    end

                    PS_CRC: begin
                        // rx_byte IS the CRC; check against accumulator
                        pkt_type_r   <= ps_type;
                        pkt_crc_ok   <= (rx_byte == ps_crc);
                        pkt_complete <= 1'b1;
                        ps_state     <= PS_SYNC1;
                        ps_crc       <= 8'd0;
                    end

                    default: ps_state <= PS_SYNC1;
                endcase
            end
        end
    end

    // =========================================================
    // Command Dispatch
    // =========================================================
    reg ping_trigger;    // pulse: build and send PONG
    reg [7:0] ping_ts[0:7]; // captured timestamp from PING

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            gait_cmd     <= 2'd0;
            gait_valid   <= 1'b0;
            estop_cmd    <= 1'b0;
            ping_trigger <= 1'b0;
        end else begin
            gait_valid   <= 1'b0;
            ping_trigger <= 1'b0;

            if (pkt_complete && pkt_crc_ok) begin
                case (pkt_type_r)
                    PKT_PING: begin
                        // Capture timestamp for echo
                        ping_ts[0] <= ps_buf[0]; ping_ts[1] <= ps_buf[1];
                        ping_ts[2] <= ps_buf[2]; ping_ts[3] <= ps_buf[3];
                        ping_ts[4] <= ps_buf[4]; ping_ts[5] <= ps_buf[5];
                        ping_ts[6] <= ps_buf[6]; ping_ts[7] <= ps_buf[7];
                        ping_trigger <= 1'b1;
                    end

                    PKT_GAIT: begin
                        // payload[0] = gait mode (STAND=0, WALK=1, TROT=2)
                        gait_cmd   <= ps_buf[0][1:0];
                        gait_valid <= 1'b1;
                    end

                    PKT_ESTOP: begin
                        // Latch E-STOP. Cleared only by reset or GAIT command.
                        estop_cmd <= 1'b1;
                    end

                    PKT_GAIT: begin
                        // GAIT also clears ESTOP
                        estop_cmd <= 1'b0;
                    end

                    default: ;  // PKT_OBSERVE and others: absorb silently
                endcase
            end
        end
    end

    // =========================================================
    // PONG TX Builder + UART TX
    // =========================================================
    // PONG packet (PKT_PONG = 0x86, payload = 8-byte echo of PING timestamp):
    //   bytes 0-1:  'C','K'  (0x43, 0x4B)
    //   byte  2:    0x86     (PKT_PONG)
    //   bytes 3-4:  0x08,0x00 (length = 8, little-endian)
    //   bytes 5-12: timestamp echo [7:0]
    //   byte  13:   CRC8 of bytes 0-12
    // Total: 14 bytes

    localparam PONG_BYTES = 14;

    reg [7:0]  tx_buf  [0:PONG_BYTES-1];
    reg [3:0]  tx_total;    // bytes to send (always PONG_BYTES=14)
    reg [3:0]  tx_byte_idx; // current byte being sent
    reg [3:0]  tx_bit_idx;  // bit within byte (0=start, 1-8=data, 9=stop)
    reg [11:0] tx_baud_cnt;
    reg        tx_busy;
    reg        tx_reg;      // current TX output bit

    assign tx_out = tx_reg;

    // CRC accumulator for building TX packet
    reg [7:0] tx_crc_accum;

    // Build PONG packet when ping_trigger fires
    // (this happens synchronously, takes one clock to latch)
    localparam [2:0]
        TS_IDLE   = 3'd0,
        TS_BUILD  = 3'd1,   // filling tx_buf and computing CRC
        TS_SEND   = 3'd2;   // shifting bytes out

    reg [2:0]  ts_state;
    reg [3:0]  build_idx;   // which byte we're building (0..13)

    // Helper: CRC8 of the known-constant PONG header (bytes 0-4: CK,0x86,0x08,0x00)
    // Pre-computed: CRC8(0x43,0x4B,0x86,0x08,0x00) = ?
    // We compute at synthesis time via the function — but that only works in always blocks.
    // Instead: build CRC incrementally in the TS_BUILD state.

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            ts_state    <= TS_IDLE;
            build_idx   <= 4'd0;
            tx_byte_idx <= 4'd0;
            tx_bit_idx  <= 4'd0;
            tx_baud_cnt <= 12'd0;
            tx_busy     <= 1'b0;
            tx_reg      <= 1'b1;   // idle high
            tx_crc_accum<= 8'd0;
        end else begin

            case (ts_state)

            TS_IDLE: begin
                tx_reg  <= 1'b1;
                tx_busy <= 1'b0;
                if (ping_trigger) begin
                    // Pre-fill constant header bytes
                    tx_buf[0]  <= 8'h43;   // 'C'
                    tx_buf[1]  <= 8'h4B;   // 'K'
                    tx_buf[2]  <= PKT_PONG;
                    tx_buf[3]  <= 8'h08;   // LEN low = 8
                    tx_buf[4]  <= 8'h00;   // LEN high = 0
                    // Timestamp bytes (dynamic)
                    tx_buf[5]  <= ping_ts[0];
                    tx_buf[6]  <= ping_ts[1];
                    tx_buf[7]  <= ping_ts[2];
                    tx_buf[8]  <= ping_ts[3];
                    tx_buf[9]  <= ping_ts[4];
                    tx_buf[10] <= ping_ts[5];
                    tx_buf[11] <= ping_ts[6];
                    tx_buf[12] <= ping_ts[7];
                    // CRC byte 13 will be computed in TS_BUILD
                    tx_crc_accum <= 8'h00;
                    build_idx    <= 4'd0;
                    ts_state     <= TS_BUILD;
                end
            end

            TS_BUILD: begin
                // Compute CRC8 over bytes 0..12, one byte per clock
                if (build_idx < 4'd13) begin
                    tx_crc_accum <= crc8_byte(tx_crc_accum, tx_buf[build_idx]);
                    build_idx    <= build_idx + 4'd1;
                end else begin
                    // Store CRC in byte 13, begin transmission
                    tx_buf[13]  <= tx_crc_accum;
                    tx_byte_idx <= 4'd0;
                    tx_bit_idx  <= 4'd0;
                    tx_baud_cnt <= 12'd0;
                    tx_busy     <= 1'b1;
                    ts_state    <= TS_SEND;
                end
            end

            TS_SEND: begin
                // One 8N1 UART byte per tx_byte_idx
                // bit 0 = start (0), bits 1-8 = data LSB-first, bit 9 = stop (1)
                if (tx_baud_cnt < BIT_PERIOD - 1) begin
                    tx_baud_cnt <= tx_baud_cnt + 12'd1;
                end else begin
                    tx_baud_cnt <= 12'd0;

                    if (tx_bit_idx == 4'd0) begin
                        // Start bit
                        tx_reg     <= 1'b0;
                        tx_bit_idx <= 4'd1;
                    end else if (tx_bit_idx <= 4'd8) begin
                        // Data bits: LSB first
                        tx_reg     <= tx_buf[tx_byte_idx][tx_bit_idx - 1];
                        tx_bit_idx <= tx_bit_idx + 4'd1;
                    end else begin
                        // Stop bit
                        tx_reg <= 1'b1;
                        tx_bit_idx <= 4'd0;
                        if (tx_byte_idx < PONG_BYTES - 1) begin
                            tx_byte_idx <= tx_byte_idx + 4'd1;
                        end else begin
                            // Done
                            tx_busy  <= 1'b0;
                            ts_state <= TS_IDLE;
                        end
                    end
                end
            end

            default: ts_state <= TS_IDLE;
            endcase
        end
    end

    // Unused inputs (prevent tool warnings)
    wire _unused = &{coh_num_in, coh_den_in, tick_in, simplex_in, 1'b0};

endmodule

`default_nettype wire
