/*
 * ck_leash_rx.v -- Δ¹ Leash UART: R16 → FPGA
 * ============================================
 * Gen12: Receives CK binary packets from R16 host.
 * Responds to PING with PONG (14-byte echo response).
 * Routes GAIT/ESTOP commands to gait controller.
 *
 * Protocol: [SYNC 'C'][SYNC 'K'][TYPE 1B][LEN_LO][LEN_HI][PAYLOAD][CRC8]
 * Baud: 115200, 8N1.  CRC8/MAXIM polynomial 0x31, init 0x00.
 *
 * PKT_PING  (0x06): respond PONG (PKT_PONG=0x86, echo 8-byte timestamp)
 * PKT_GAIT  (0x23): gait_cmd[1:0] ← payload[0][1:0], gait_valid pulse
 * PKT_ESTOP (0x2E): estop_cmd ← 1 (cleared by GAIT or reset)
 * Others:  silently absorbed
 *
 * tx_out is idle-high UART. AND with servo_tx at top level for shared bus.
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

    input  wire        uart_rx,       // UART RX from R16 (idle-high)

    output reg  [1:0]  gait_cmd,      // decoded gait mode
    output reg         gait_valid,    // one-cycle pulse
    output reg         estop_cmd,     // level: R16 E-STOP active

    input  wire [15:0] coh_num_in,    // (reserved for future STATE response)
    input  wire [15:0] coh_den_in,
    input  wire [31:0] tick_in,
    input  wire [1:0]  simplex_in,

    output wire        tx_out         // UART TX (idle-high, shared bus)
);

    // ── Baud constants ───────────────────────────────────────────────────
    localparam integer BIT_PER  = CLK_FREQ / BAUD;   // 434 clocks/bit @ 50M/115200
    localparam integer HALF_PER = BIT_PER / 2;       // 217

    // ── Packet type codes ────────────────────────────────────────────────
    localparam [7:0] PKT_PING  = 8'h06;
    localparam [7:0] PKT_GAIT  = 8'h23;
    localparam [7:0] PKT_ESTOP = 8'h2E;
    localparam [7:0] PKT_PONG  = 8'h86;

    // ── UART RX ──────────────────────────────────────────────────────────
    reg [1:0]  rx_sync;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) rx_sync <= 2'b11;
        else        rx_sync <= {rx_sync[0], uart_rx};
    end
    wire rx_in = rx_sync[1];

    // Standard 8N1 byte receiver
    reg [11:0] rx_cnt;
    reg [3:0]  rx_bits;
    reg [7:0]  rx_sr;
    reg        rx_busy;
    reg        rx_vld;
    reg [7:0]  rx_byte;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            rx_cnt  <= 12'd0; rx_bits <= 4'd0;
            rx_sr   <= 8'h00; rx_busy <= 1'b0;
            rx_vld  <= 1'b0;  rx_byte <= 8'h00;
        end else begin
            rx_vld <= 1'b0;
            if (!rx_busy) begin
                if (!rx_in) begin           // falling edge = start bit
                    rx_busy <= 1'b1;
                    rx_cnt  <= 12'd0;
                    rx_bits <= 4'd0;
                end
            end else begin
                if (rx_cnt < BIT_PER - 1) begin
                    rx_cnt <= rx_cnt + 12'd1;
                end else begin
                    rx_cnt <= 12'd0;
                    if (rx_bits == 4'd0) begin
                        // Skip start bit center, move to bit 1
                        rx_bits <= 4'd1;
                    end else if (rx_bits <= 4'd8) begin
                        rx_sr   <= {rx_in, rx_sr[7:1]};   // LSB first
                        rx_bits <= rx_bits + 4'd1;
                    end else begin
                        // Stop bit
                        if (rx_in) begin
                            rx_byte <= rx_sr;
                            rx_vld  <= 1'b1;
                        end
                        rx_busy <= 1'b0;
                        rx_bits <= 4'd0;
                    end
                end
            end
        end
    end

    // ── CRC-8/MAXIM (poly 0x31) ──────────────────────────────────────────
    // Updated byte by byte with intermediate register
    function [7:0] crc8_update;
        input [7:0] crc_in;
        input [7:0] din;
        reg [7:0] c;
        integer  k;
        begin
            c = crc_in ^ din;
            for (k = 0; k < 8; k = k + 1)
                c = c[7] ? {c[6:0], 1'b0} ^ 8'h31 : {c[6:0], 1'b0};
            crc8_update = c;
        end
    endfunction

    // ── Packet parser state machine ───────────────────────────────────────
    localparam [2:0]
        PS_S1  = 3'd0,   // wait for 'C'
        PS_S2  = 3'd1,   // wait for 'K'
        PS_TY  = 3'd2,   // type byte
        PS_LL  = 3'd3,   // length low
        PS_LH  = 3'd4,   // length high
        PS_PL  = 3'd5,   // payload bytes
        PS_CR  = 3'd6;   // crc byte

    reg [2:0]  ps;
    reg [7:0]  p_type;
    reg [7:0]  p_len;        // capped payload length
    reg [7:0]  p_full_len;   // declared payload length
    reg [7:0]  p_idx;
    reg [7:0]  crc_acc;

    // Payload buffer – max 8 bytes (enough for PING 8-byte timestamp)
    reg [7:0]  pbuf0, pbuf1, pbuf2, pbuf3;
    reg [7:0]  pbuf4, pbuf5, pbuf6, pbuf7;

    // Dispatch signals
    reg        pkt_ok;       // pulse: good packet
    reg [7:0]  pkt_type_r;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            ps       <= PS_S1;
            p_type   <= 8'd0; p_len <= 8'd0; p_full_len <= 8'd0;
            p_idx    <= 8'd0; crc_acc <= 8'd0;
            pbuf0 <= 8'd0; pbuf1 <= 8'd0; pbuf2 <= 8'd0; pbuf3 <= 8'd0;
            pbuf4 <= 8'd0; pbuf5 <= 8'd0; pbuf6 <= 8'd0; pbuf7 <= 8'd0;
            pkt_ok   <= 1'b0; pkt_type_r <= 8'd0;
        end else begin
            pkt_ok <= 1'b0;
            if (rx_vld) begin
                case (ps)
                    PS_S1: begin
                        if (rx_byte == 8'h43) begin   // 'C'
                            crc_acc <= crc8_update(8'h00, rx_byte);
                            ps <= PS_S2;
                        end
                    end
                    PS_S2: begin
                        if (rx_byte == 8'h4B) begin   // 'K'
                            crc_acc <= crc8_update(crc_acc, rx_byte);
                            ps <= PS_TY;
                        end else if (rx_byte == 8'h43) begin
                            crc_acc <= crc8_update(8'h00, rx_byte);
                        end else begin
                            ps <= PS_S1;
                        end
                    end
                    PS_TY: begin
                        p_type  <= rx_byte;
                        crc_acc <= crc8_update(crc_acc, rx_byte);
                        ps <= PS_LL;
                    end
                    PS_LL: begin
                        p_full_len <= rx_byte;
                        crc_acc    <= crc8_update(crc_acc, rx_byte);
                        ps <= PS_LH;
                    end
                    PS_LH: begin
                        crc_acc <= crc8_update(crc_acc, rx_byte);
                        // Cap at 8 bytes; ignore high length byte
                        if (p_full_len == 8'd0) begin
                            p_len  <= 8'd0;
                            p_idx  <= 8'd0;
                            ps <= PS_CR;
                        end else begin
                            p_len  <= (p_full_len > 8'd8) ? 8'd8 : p_full_len;
                            p_idx  <= 8'd0;
                            ps <= PS_PL;
                        end
                    end
                    PS_PL: begin
                        crc_acc <= crc8_update(crc_acc, rx_byte);
                        // Store up to 8 payload bytes (flat regs, no array)
                        if (p_idx == 8'd0) pbuf0 <= rx_byte;
                        if (p_idx == 8'd1) pbuf1 <= rx_byte;
                        if (p_idx == 8'd2) pbuf2 <= rx_byte;
                        if (p_idx == 8'd3) pbuf3 <= rx_byte;
                        if (p_idx == 8'd4) pbuf4 <= rx_byte;
                        if (p_idx == 8'd5) pbuf5 <= rx_byte;
                        if (p_idx == 8'd6) pbuf6 <= rx_byte;
                        if (p_idx == 8'd7) pbuf7 <= rx_byte;
                        p_idx <= p_idx + 8'd1;
                        if (p_idx + 8'd1 >= p_full_len)
                            ps <= PS_CR;
                    end
                    PS_CR: begin
                        pkt_type_r <= p_type;
                        pkt_ok     <= (rx_byte == crc_acc);
                        ps         <= PS_S1;
                        crc_acc    <= 8'd0;
                    end
                    default: ps <= PS_S1;
                endcase
            end
        end
    end

    // ── Command dispatch ──────────────────────────────────────────────────
    reg        ping_go;           // pulse: start PONG TX
    reg [7:0]  pts0, pts1, pts2, pts3;   // captured PING timestamp
    reg [7:0]  pts4, pts5, pts6, pts7;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            gait_cmd  <= 2'd0; gait_valid <= 1'b0;
            estop_cmd <= 1'b0; ping_go    <= 1'b0;
            pts0 <= 8'd0; pts1 <= 8'd0; pts2 <= 8'd0; pts3 <= 8'd0;
            pts4 <= 8'd0; pts5 <= 8'd0; pts6 <= 8'd0; pts7 <= 8'd0;
        end else begin
            gait_valid <= 1'b0;
            ping_go    <= 1'b0;
            if (pkt_ok) begin
                case (pkt_type_r)
                    PKT_PING: begin
                        pts0 <= pbuf0; pts1 <= pbuf1;
                        pts2 <= pbuf2; pts3 <= pbuf3;
                        pts4 <= pbuf4; pts5 <= pbuf5;
                        pts6 <= pbuf6; pts7 <= pbuf7;
                        ping_go <= 1'b1;
                    end
                    PKT_GAIT: begin
                        gait_cmd   <= pbuf0[1:0];
                        gait_valid <= 1'b1;
                        estop_cmd  <= 1'b0;
                    end
                    PKT_ESTOP: begin
                        estop_cmd <= 1'b1;
                    end
                    default: ;
                endcase
            end
        end
    end

    // ── PONG TX: 14-byte packet ───────────────────────────────────────────
    // Packet: 0x43,0x4B,0x86,0x08,0x00,[ts0..ts7],[crc8]
    // We build it into flat regs and shift out byte-by-byte via UART TX.

    localparam [3:0]
        TS_IDLE  = 4'd0,
        TS_B0    = 4'd1,   // byte 0  = 0x43
        TS_B1    = 4'd2,
        TS_B2    = 4'd3,
        TS_B3    = 4'd4,
        TS_B4    = 4'd5,
        TS_B5    = 4'd6,   // ts[0]
        TS_B6    = 4'd7,
        TS_B7    = 4'd8,
        TS_B8    = 4'd9,
        TS_B9    = 4'd10,
        TS_B10   = 4'd11,
        TS_B11   = 4'd12,
        TS_B12   = 4'd13;  // ts[7]
        // CRC byte sent in TS_IDLE→TS_B0 transition after crc ready

    // Build packet bytes in regs; shift out via UART TX
    // Use a small FSM: state counts bytes 0..13, then done

    // CRC over header+ts (computed combinatorially from pts regs after ping_go)
    // We compute it in a pipeline of 13 clock cycles during TS_BUILD state

    localparam [2:0]
        TX_IDLE  = 3'd0,
        TX_BUILD = 3'd1,   // compute CRC byte-by-byte
        TX_SEND  = 3'd2;   // shift out bytes via UART

    // 14 packet bytes stored flat
    reg [7:0]  tb0,  tb1,  tb2,  tb3,  tb4,  tb5,  tb6;
    reg [7:0]  tb7,  tb8,  tb9,  tb10, tb11, tb12, tb13;

    reg [2:0]  tx_st;
    reg [3:0]  tx_bidx;    // byte index 0..13
    reg [3:0]  tx_bcnt;    // build index 0..12 (for CRC)
    reg [7:0]  tx_crc;     // running CRC during build
    reg [7:0]  tx_cur;     // current byte being sent

    // UART TX shift register
    reg [3:0]  tx_bit;     // 0=start, 1-8=data, 9=stop
    reg [11:0] tx_cnt;
    reg        tx_reg;

    assign tx_out = tx_reg;

    // Mux to read tx_buf by index (flat regs need explicit mux)
    function [7:0] pong_byte;
        input [3:0] idx;
        begin
            case (idx)
                4'd0:  pong_byte = 8'h43;
                4'd1:  pong_byte = 8'h4B;
                4'd2:  pong_byte = PKT_PONG;
                4'd3:  pong_byte = 8'h08;
                4'd4:  pong_byte = 8'h00;
                4'd5:  pong_byte = 8'h00;  // ts0 (filled after build)
                4'd6:  pong_byte = 8'h00;  // ts1
                4'd7:  pong_byte = 8'h00;  // ts2
                4'd8:  pong_byte = 8'h00;  // ts3
                4'd9:  pong_byte = 8'h00;  // ts4
                4'd10: pong_byte = 8'h00;  // ts5
                4'd11: pong_byte = 8'h00;  // ts6
                4'd12: pong_byte = 8'h00;  // ts7
                4'd13: pong_byte = 8'h00;  // crc (filled after build)
                default: pong_byte = 8'h00;
            endcase
        end
    endfunction

    // Build index → byte value (uses captured pts regs)
    function [7:0] build_byte;
        input [3:0] idx;
        input [7:0] t0, t1, t2, t3, t4, t5, t6, t7;
        begin
            case (idx)
                4'd0:  build_byte = 8'h43;
                4'd1:  build_byte = 8'h4B;
                4'd2:  build_byte = PKT_PONG;
                4'd3:  build_byte = 8'h08;
                4'd4:  build_byte = 8'h00;
                4'd5:  build_byte = t0;
                4'd6:  build_byte = t1;
                4'd7:  build_byte = t2;
                4'd8:  build_byte = t3;
                4'd9:  build_byte = t4;
                4'd10: build_byte = t5;
                4'd11: build_byte = t6;
                4'd12: build_byte = t7;
                default: build_byte = 8'h00;
            endcase
        end
    endfunction

    // TX flat-reg mux (after build, tb regs hold final bytes)
    function [7:0] tx_byte_mux;
        input [3:0] idx;
        input [7:0] b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13;
        begin
            case (idx)
                4'd0:  tx_byte_mux = b0;  4'd1:  tx_byte_mux = b1;
                4'd2:  tx_byte_mux = b2;  4'd3:  tx_byte_mux = b3;
                4'd4:  tx_byte_mux = b4;  4'd5:  tx_byte_mux = b5;
                4'd6:  tx_byte_mux = b6;  4'd7:  tx_byte_mux = b7;
                4'd8:  tx_byte_mux = b8;  4'd9:  tx_byte_mux = b9;
                4'd10: tx_byte_mux = b10; 4'd11: tx_byte_mux = b11;
                4'd12: tx_byte_mux = b12; 4'd13: tx_byte_mux = b13;
                default: tx_byte_mux = 8'hFF;
            endcase
        end
    endfunction

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            tx_st   <= TX_IDLE; tx_bidx <= 4'd0; tx_bcnt <= 4'd0;
            tx_crc  <= 8'd0;    tx_cur  <= 8'hFF;
            tx_bit  <= 4'd0;    tx_cnt  <= 12'd0; tx_reg <= 1'b1;
            tb0 <=8'h43; tb1 <=8'h4B; tb2 <=PKT_PONG;
            tb3 <=8'h08; tb4 <=8'h00; tb5 <=8'h00;
            tb6 <=8'h00; tb7 <=8'h00; tb8 <=8'h00;
            tb9 <=8'h00; tb10<=8'h00; tb11<=8'h00;
            tb12<=8'h00; tb13<=8'h00;
        end else begin
            case (tx_st)

            TX_IDLE: begin
                tx_reg <= 1'b1;
                if (ping_go) begin
                    // Latch constant header + timestamp
                    tb0  <= 8'h43;   tb1  <= 8'h4B;
                    tb2  <= PKT_PONG; tb3  <= 8'h08;
                    tb4  <= 8'h00;   tb5  <= pts0;
                    tb6  <= pts1;    tb7  <= pts2;
                    tb8  <= pts3;    tb9  <= pts4;
                    tb10 <= pts5;    tb11 <= pts6;
                    tb12 <= pts7;    // tb13 = CRC, computed in BUILD
                    tx_crc  <= 8'h00;
                    tx_bcnt <= 4'd0;
                    tx_st   <= TX_BUILD;
                end
            end

            TX_BUILD: begin
                // Compute CRC8 over bytes 0..12 (one per clock)
                if (tx_bcnt <= 4'd12) begin
                    tx_crc  <= crc8_update(tx_crc,
                                   build_byte(tx_bcnt,
                                     pts0,pts1,pts2,pts3,pts4,pts5,pts6,pts7));
                    tx_bcnt <= tx_bcnt + 4'd1;
                end else begin
                    tb13   <= tx_crc;      // store final CRC
                    tx_bidx <= 4'd0;
                    tx_bit  <= 4'd0;
                    tx_cnt  <= 12'd0;
                    tx_cur  <= 8'h43;      // first byte = 'C'
                    tx_st   <= TX_SEND;
                end
            end

            TX_SEND: begin
                if (tx_cnt < BIT_PER - 1) begin
                    tx_cnt <= tx_cnt + 12'd1;
                end else begin
                    tx_cnt <= 12'd0;
                    if (tx_bit == 4'd0) begin
                        tx_reg <= 1'b0;       // start bit
                        tx_bit <= 4'd1;
                    end else if (tx_bit <= 4'd8) begin
                        tx_reg <= tx_cur[tx_bit - 4'd1];  // data LSB first
                        tx_bit <= tx_bit + 4'd1;
                    end else begin
                        tx_reg <= 1'b1;       // stop bit
                        tx_bit <= 4'd0;
                        if (tx_bidx < 4'd13) begin
                            tx_bidx <= tx_bidx + 4'd1;
                            tx_cur  <= tx_byte_mux(tx_bidx + 4'd1,
                                         tb0,tb1,tb2,tb3,tb4,tb5,tb6,
                                         tb7,tb8,tb9,tb10,tb11,tb12,tb13);
                        end else begin
                            tx_st <= TX_IDLE;  // all 14 bytes sent
                        end
                    end
                end
            end

            default: tx_st <= TX_IDLE;
            endcase
        end
    end

    // Prevent unused-port warnings
    wire _unused = &{coh_num_in, coh_den_in, tick_in, simplex_in, 1'b0};

endmodule

`default_nettype wire
