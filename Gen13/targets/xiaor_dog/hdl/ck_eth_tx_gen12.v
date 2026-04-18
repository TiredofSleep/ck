/*
 * ck_eth_tx_gen12.v -- Gen12 PL RGMII Ethernet TX (12-byte payload)
 * ==================================================================
 * Extended from ck_eth_tx.v (Gen9/10/11 — 10-byte payload).
 *
 * Gen12 changes:
 *   - phase_bc[3:0] replaced by simplex_state[1:0]  (Δ⁰/Δ¹/Δ²/Δ³ layer)
 *   - gap_position[15:0] added               (HD position in bridge zone)
 *   - Payload 10 bytes → 12 bytes
 *   - IP total length 38 → 40
 *   - UDP length 18 → 20
 *   - Pad reduced from 8 to 6 bytes
 *
 * Gen12 payload layout (12 bytes, offset from UDP payload start):
 *   [0-3]  tick_count[31:0]          big-endian
 *   [4]    {2'b00, simplex_state[1:0], fuse_op[3:0]}
 *   [5-6]  coh_num[15:0]             big-endian
 *   [7-8]  coh_den[15:0]             big-endian
 *   [9]    {7'd0, bump}
 *   [10-11] gap_position[15:0]       big-endian  ← NEW
 *
 * Everything else identical to ck_eth_tx.v:
 *   MMCM 50→125 MHz, RGMII DDR, MDIO RTL8211F init, CRC-32, fixed MAC/IP.
 *
 * (c) 2026 Brayden Ross Sanders / 7Site LLC — Trinity Infinity Geometry
 * Authors: Brayden Ross Sanders & Monica
 */

module ck_eth_tx_gen12 (
    input  wire        clk_50m,

    input  wire        rst_n,

    // Heartbeat inputs (50 MHz domain)
    input  wire        tick_done,
    input  wire [31:0] tick_count,
    input  wire [1:0]  simplex_state,   // Gen12: Δ layer (was phase_bc[3:0])
    input  wire [15:0] gap_position,    // Gen12: HD position in bridge zone (NEW)
    input  wire [3:0]  fuse_op,
    input  wire [15:0] coh_num,
    input  wire [15:0] coh_den,
    input  wire        bump,

    // RGMII PHY
    output wire        phy_gtx_clk,
    output wire [3:0]  phy_txd,
    output wire        phy_tx_en,
    output wire        phy_mdc,
    inout  wire        phy_mdio,

    // Status
    output wire        mmcm_locked,
    output wire        link_ready
);

    // =========================================================
    // MMCM: 50 MHz → 125 MHz
    // =========================================================
    wire clk_125, clk_fb, mmcm_lock_i;

    MMCME2_BASE #(
        .CLKIN1_PERIOD  (20.000),
        .CLKFBOUT_MULT_F(25.0),
        .CLKOUT0_DIVIDE_F(10.0)
    ) mmcm_eth (
        .CLKIN1   (clk_50m),
        .RST      (~rst_n),
        .PWRDWN   (1'b0),
        .CLKFBIN  (clk_fb),
        .CLKFBOUT (clk_fb),
        .CLKOUT0  (clk_125),
        .LOCKED   (mmcm_lock_i),
        .CLKOUT0B (), .CLKOUT1 (), .CLKOUT1B(),
        .CLKOUT2  (), .CLKOUT2B(), .CLKOUT3 (),
        .CLKOUT3B (), .CLKOUT4 (), .CLKOUT5 (),
        .CLKOUT6  (), .CLKFBOUTB()
    );

    assign mmcm_locked = mmcm_lock_i;

    wire clk_tx;
    BUFG bufg_tx (.I(clk_125), .O(clk_tx));
    wire tx_rst_n = rst_n & mmcm_lock_i;

    // =========================================================
    // Sync tick_done 50MHz → 125MHz + latch payload
    // =========================================================
    reg [2:0] td_sync;
    always @(posedge clk_tx or negedge tx_rst_n) begin
        if (!tx_rst_n) td_sync <= 3'b0;
        else           td_sync <= {td_sync[1:0], tick_done};
    end
    wire td_rise = td_sync[1] & ~td_sync[2];

    reg [31:0] lat_tick;
    reg [1:0]  lat_simplex;
    reg [15:0] lat_gap;
    reg [3:0]  lat_fuse;
    reg [15:0] lat_coh_num, lat_coh_den;
    reg        lat_bump;

    always @(posedge clk_50m or negedge rst_n) begin
        if (!rst_n) begin
            lat_tick    <= 32'd0; lat_simplex <= 2'd0; lat_gap     <= 16'd0;
            lat_fuse    <= 4'd0;  lat_coh_num <= 16'd0; lat_coh_den <= 16'd0;
            lat_bump    <= 1'b0;
        end else if (tick_done) begin
            lat_tick    <= tick_count;  lat_simplex <= simplex_state;
            lat_gap     <= gap_position; lat_fuse   <= fuse_op;
            lat_coh_num <= coh_num;     lat_coh_den <= coh_den;
            lat_bump    <= bump;
        end
    end

    reg [31:0] tx_tick;
    reg [1:0]  tx_simplex;
    reg [15:0] tx_gap;
    reg [3:0]  tx_fuse;
    reg [15:0] tx_coh_num, tx_coh_den;
    reg        tx_bump;

    always @(posedge clk_tx) begin
        tx_tick    <= lat_tick;    tx_simplex <= lat_simplex;
        tx_gap     <= lat_gap;     tx_fuse    <= lat_fuse;
        tx_coh_num <= lat_coh_num; tx_coh_den <= lat_coh_den;
        tx_bump    <= lat_bump;
    end

    // =========================================================
    // MDIO Controller — init RTL8211F (identical to Gen9)
    // =========================================================
    localparam MDIO_PRE = 32'hFFFF_FFFF;
    localparam PHY_ADDR = 5'b00001;

    localparam [2:0] MDIO_IDLE  = 3'd0, MDIO_WRITE = 3'd1, MDIO_WAIT  = 3'd2,
                     MDIO_NEXT  = 3'd3, MDIO_DONE  = 3'd4;

    reg [4:0]  mdio_reg  [0:2];
    reg [15:0] mdio_data [0:2];
    reg [1:0]  mdio_idx;

    initial begin
        mdio_reg[0] = 5'd31; mdio_data[0] = 16'h0D08;
        mdio_reg[1] = 5'd17; mdio_data[1] = 16'h0108;
        mdio_reg[2] = 5'd31; mdio_data[2] = 16'h0000;
    end

    reg [2:0]  mdio_state;
    reg [6:0]  mdio_clk_div;
    reg        mdio_clk_en;
    reg [5:0]  mdio_bit_cnt;
    reg [63:0] mdio_shift;
    reg        mdio_oe, mdio_out;
    reg [15:0] mdio_pause_cnt;
    reg        mdio_init_done;

    assign phy_mdc  = mdio_clk_div[6];
    assign phy_mdio = mdio_oe ? mdio_out : 1'bz;
    assign link_ready = mdio_init_done;

    always @(posedge clk_50m or negedge rst_n) begin
        if (!rst_n) begin
            mdio_clk_div <= 7'd0; mdio_clk_en <= 1'b0;
        end else begin
            mdio_clk_div <= mdio_clk_div + 7'd1;
            mdio_clk_en  <= (mdio_clk_div == 7'd63);
        end
    end

    always @(posedge clk_50m or negedge rst_n) begin
        if (!rst_n) begin
            mdio_state <= MDIO_IDLE; mdio_idx <= 2'd0; mdio_bit_cnt <= 6'd0;
            mdio_shift <= 64'd0; mdio_oe <= 1'b0; mdio_out <= 1'b1;
            mdio_pause_cnt <= 16'd0; mdio_init_done <= 1'b0;
        end else if (mdio_clk_en) begin
            case (mdio_state)
                MDIO_IDLE: begin
                    mdio_pause_cnt <= mdio_pause_cnt + 16'd1;
                    if (mdio_pause_cnt == 16'd50000) begin
                        mdio_state <= MDIO_WRITE; mdio_bit_cnt <= 6'd0;
                        mdio_shift <= {MDIO_PRE, 2'b01, 2'b01, PHY_ADDR,
                                       mdio_reg[0], 2'b10, mdio_data[0]};
                        mdio_oe <= 1'b1;
                    end
                end
                MDIO_WRITE: begin
                    mdio_out <= mdio_shift[63];
                    mdio_shift <= {mdio_shift[62:0], 1'b1};
                    mdio_bit_cnt <= mdio_bit_cnt + 6'd1;
                    if (mdio_bit_cnt == 6'd63) begin
                        mdio_state <= MDIO_WAIT; mdio_oe <= 1'b0;
                        mdio_out <= 1'b1; mdio_pause_cnt <= 16'd0;
                    end
                end
                MDIO_WAIT: begin
                    mdio_pause_cnt <= mdio_pause_cnt + 16'd1;
                    if (mdio_pause_cnt == 16'd64) mdio_state <= MDIO_NEXT;
                end
                MDIO_NEXT: begin
                    if (mdio_idx == 2'd2) begin
                        mdio_state <= MDIO_DONE; mdio_init_done <= 1'b1;
                    end else begin
                        mdio_idx <= mdio_idx + 2'd1;
                        mdio_state <= MDIO_WRITE; mdio_bit_cnt <= 6'd0;
                        mdio_shift <= {MDIO_PRE, 2'b01, 2'b01, PHY_ADDR,
                                       mdio_reg[mdio_idx + 2'd1], 2'b10,
                                       mdio_data[mdio_idx + 2'd1]};
                        mdio_oe <= 1'b1;
                    end
                end
                MDIO_DONE: begin mdio_oe <= 1'b0; mdio_out <= 1'b1; end
            endcase
        end
    end

    // =========================================================
    // Ethernet Frame Builder (TX state machine)
    // =========================================================
    localparam [47:0] DST_MAC = 48'hFFFF_FFFF_FFFF;
    localparam [47:0] SRC_MAC = 48'h7E_C4_5A_00_77_77;
    localparam [31:0] SRC_IP  = {8'd192, 8'd168, 8'd1, 8'd100};
    localparam [31:0] DST_IP  = {8'd192, 8'd168, 8'd1, 8'd255};
    localparam [15:0] SRC_PORT = 16'd7777, DST_PORT = 16'd7777;

    // Gen12: payload = 12, UDP = 8+12 = 20, IP = 20+20 = 40
    localparam [15:0] UDP_LEN      = 16'd20;
    localparam [15:0] IP_TOTAL_LEN = 16'd40;  // was 38 in Gen9

    // IP header checksum (Gen12: total length 0x0028 instead of 0x0026)
    wire [16:0] ip_fold1 = {1'b0, 16'h4500} + {1'b0, IP_TOTAL_LEN}
                         + {1'b0, 16'h0000} + {1'b0, 16'h4000}
                         + {1'b0, 16'h4011}
                         + {1'b0, SRC_IP[31:16]} + {1'b0, SRC_IP[15:0]}
                         + {1'b0, DST_IP[31:16]} + {1'b0, DST_IP[15:0]};
    // Fold carries
    wire [16:0] ip_fold2 = {1'b0, ip_fold1[15:0]} + {16'd0, ip_fold1[16]};
    wire [15:0] ip_cksum = ~ip_fold2[15:0];

    localparam [2:0] ST_IDLE     = 3'd0, ST_BUILD    = 3'd1, ST_CRC      = 3'd2,
                     ST_PREAMBLE = 3'd3, ST_FRAME     = 3'd4, ST_FCS      = 3'd5,
                     ST_IFG      = 3'd6;

    reg [2:0] tx_state;
    reg [7:0] frame_buf [0:59];   // 60 bytes (DstMAC..Pad, no FCS)
    reg [6:0] tx_byte_cnt;

    reg [31:0] crc_reg;

    reg [3:0] rgmii_txd_r, rgmii_txd_f;
    reg       rgmii_txen_r, rgmii_txen_f;

    // CRC-32 (IEEE 802.3)
    function [31:0] crc32_byte;
        input [31:0] crc_in;
        input [7:0]  data_in;
        reg [31:0] c; reg [7:0] d; integer j;
        begin
            c = crc_in; d = data_in;
            for (j = 0; j < 8; j = j + 1) begin
                if ((c[0] ^ d[0]) == 1'b1) c = {1'b0, c[31:1]} ^ 32'hEDB88320;
                else                        c = {1'b0, c[31:1]};
                d = {1'b0, d[7:1]};
            end
            crc32_byte = c;
        end
    endfunction

    always @(posedge clk_tx or negedge tx_rst_n) begin
        if (!tx_rst_n) begin
            tx_state     <= ST_IDLE; tx_byte_cnt <= 7'd0;
            crc_reg      <= 32'hFFFF_FFFF;
            rgmii_txd_r  <= 4'd0; rgmii_txd_f  <= 4'd0;
            rgmii_txen_r <= 1'b0; rgmii_txen_f <= 1'b0;
        end else begin
            case (tx_state)

            ST_IDLE: begin
                rgmii_txen_r <= 1'b0; rgmii_txen_f <= 1'b0;
                rgmii_txd_r  <= 4'd0; rgmii_txd_f  <= 4'd0;
                if (td_rise && mdio_init_done) begin
                    tx_state <= ST_BUILD; tx_byte_cnt <= 7'd0;
                end
            end

            ST_BUILD: begin
                // ── Destination / Source MACs (bytes 0-11) ──
                frame_buf[0]  <= DST_MAC[47:40]; frame_buf[1]  <= DST_MAC[39:32];
                frame_buf[2]  <= DST_MAC[31:24]; frame_buf[3]  <= DST_MAC[23:16];
                frame_buf[4]  <= DST_MAC[15:8];  frame_buf[5]  <= DST_MAC[7:0];
                frame_buf[6]  <= SRC_MAC[47:40]; frame_buf[7]  <= SRC_MAC[39:32];
                frame_buf[8]  <= SRC_MAC[31:24]; frame_buf[9]  <= SRC_MAC[23:16];
                frame_buf[10] <= SRC_MAC[15:8];  frame_buf[11] <= SRC_MAC[7:0];
                // ── EtherType: IPv4 (bytes 12-13) ──
                frame_buf[12] <= 8'h08; frame_buf[13] <= 8'h00;
                // ── IP Header (bytes 14-33) ──
                frame_buf[14] <= 8'h45; frame_buf[15] <= 8'h00;
                frame_buf[16] <= IP_TOTAL_LEN[15:8]; frame_buf[17] <= IP_TOTAL_LEN[7:0];
                frame_buf[18] <= 8'h00; frame_buf[19] <= 8'h00;
                frame_buf[20] <= 8'h40; frame_buf[21] <= 8'h00;
                frame_buf[22] <= 8'h40; frame_buf[23] <= 8'h11;
                frame_buf[24] <= ip_cksum[15:8]; frame_buf[25] <= ip_cksum[7:0];
                frame_buf[26] <= SRC_IP[31:24]; frame_buf[27] <= SRC_IP[23:16];
                frame_buf[28] <= SRC_IP[15:8];  frame_buf[29] <= SRC_IP[7:0];
                frame_buf[30] <= DST_IP[31:24]; frame_buf[31] <= DST_IP[23:16];
                frame_buf[32] <= DST_IP[15:8];  frame_buf[33] <= DST_IP[7:0];
                // ── UDP Header (bytes 34-41) ──
                frame_buf[34] <= SRC_PORT[15:8]; frame_buf[35] <= SRC_PORT[7:0];
                frame_buf[36] <= DST_PORT[15:8]; frame_buf[37] <= DST_PORT[7:0];
                frame_buf[38] <= UDP_LEN[15:8];  frame_buf[39] <= UDP_LEN[7:0];
                frame_buf[40] <= 8'h00;          frame_buf[41] <= 8'h00;
                // ── Gen12 Payload (bytes 42-53, 12 bytes) ──
                frame_buf[42] <= tx_tick[31:24];
                frame_buf[43] <= tx_tick[23:16];
                frame_buf[44] <= tx_tick[15:8];
                frame_buf[45] <= tx_tick[7:0];
                frame_buf[46] <= {2'b00, tx_simplex, tx_fuse};  // state[5:4] fuse[3:0]
                frame_buf[47] <= tx_coh_num[15:8];
                frame_buf[48] <= tx_coh_num[7:0];
                frame_buf[49] <= tx_coh_den[15:8];
                frame_buf[50] <= tx_coh_den[7:0];
                frame_buf[51] <= {7'd0, tx_bump};
                frame_buf[52] <= tx_gap[15:8];   // gap_position MSB ← NEW
                frame_buf[53] <= tx_gap[7:0];    // gap_position LSB ← NEW
                // ── Pad (bytes 54-59, 6 bytes — reduced from 8 in Gen9) ──
                frame_buf[54] <= 8'h00; frame_buf[55] <= 8'h00;
                frame_buf[56] <= 8'h00; frame_buf[57] <= 8'h00;
                frame_buf[58] <= 8'h00; frame_buf[59] <= 8'h00;

                tx_state <= ST_CRC; tx_byte_cnt <= 7'd0;
                crc_reg  <= 32'hFFFF_FFFF;
            end

            ST_CRC: begin
                if (tx_byte_cnt < 7'd60) begin
                    crc_reg     <= crc32_byte(crc_reg, frame_buf[tx_byte_cnt]);
                    tx_byte_cnt <= tx_byte_cnt + 7'd1;
                end else begin
                    tx_state <= ST_PREAMBLE; tx_byte_cnt <= 7'd0;
                end
            end

            ST_PREAMBLE: begin
                rgmii_txen_r <= 1'b1; rgmii_txen_f <= 1'b0;
                if (tx_byte_cnt < 7'd7) begin
                    rgmii_txd_r <= 4'h5; rgmii_txd_f <= 4'h5;
                    tx_byte_cnt <= tx_byte_cnt + 7'd1;
                end else begin
                    rgmii_txd_r <= 4'h5; rgmii_txd_f <= 4'hD;  // SFD 0xD5
                    tx_byte_cnt <= 7'd0; tx_state <= ST_FRAME;
                end
            end

            ST_FRAME: begin
                rgmii_txen_r <= 1'b1; rgmii_txen_f <= 1'b0;
                rgmii_txd_r  <= frame_buf[tx_byte_cnt][3:0];
                rgmii_txd_f  <= frame_buf[tx_byte_cnt][7:4];
                tx_byte_cnt  <= tx_byte_cnt + 7'd1;
                if (tx_byte_cnt == 7'd59) begin
                    tx_state <= ST_FCS; tx_byte_cnt <= 7'd0;
                end
            end

            ST_FCS: begin
                rgmii_txen_r <= 1'b1; rgmii_txen_f <= 1'b0;
                case (tx_byte_cnt[1:0])
                    2'd0: begin rgmii_txd_r <= ~crc_reg[3:0];   rgmii_txd_f <= ~crc_reg[7:4];   end
                    2'd1: begin rgmii_txd_r <= ~crc_reg[11:8];  rgmii_txd_f <= ~crc_reg[15:12]; end
                    2'd2: begin rgmii_txd_r <= ~crc_reg[19:16]; rgmii_txd_f <= ~crc_reg[23:20]; end
                    2'd3: begin rgmii_txd_r <= ~crc_reg[27:24]; rgmii_txd_f <= ~crc_reg[31:28]; end
                endcase
                tx_byte_cnt <= tx_byte_cnt + 7'd1;
                if (tx_byte_cnt == 7'd3) begin
                    tx_state <= ST_IFG; tx_byte_cnt <= 7'd0;
                end
            end

            ST_IFG: begin
                rgmii_txen_r <= 1'b0; rgmii_txen_f <= 1'b0;
                rgmii_txd_r  <= 4'd0; rgmii_txd_f  <= 4'd0;
                tx_byte_cnt  <= tx_byte_cnt + 7'd1;
                if (tx_byte_cnt == 7'd11) tx_state <= ST_IDLE;
            end

            endcase
        end
    end

    // =========================================================
    // RGMII ODDR Primitives (identical to Gen9)
    // =========================================================
    ODDR #(.DDR_CLK_EDGE("SAME_EDGE"), .INIT(1'b0), .SRTYPE("ASYNC")) oddr_gtx_clk (
        .Q(phy_gtx_clk), .C(clk_tx), .CE(1'b1),
        .D1(1'b1), .D2(1'b0), .R(~tx_rst_n), .S(1'b0));

    genvar gi;
    generate
        for (gi = 0; gi < 4; gi = gi + 1) begin : gen_txd_oddr
            ODDR #(.DDR_CLK_EDGE("SAME_EDGE"), .INIT(1'b0), .SRTYPE("ASYNC")) oddr_txd (
                .Q(phy_txd[gi]), .C(clk_tx), .CE(1'b1),
                .D1(rgmii_txd_r[gi]), .D2(rgmii_txd_f[gi]),
                .R(~tx_rst_n), .S(1'b0));
        end
    endgenerate

    ODDR #(.DDR_CLK_EDGE("SAME_EDGE"), .INIT(1'b0), .SRTYPE("ASYNC")) oddr_tx_en (
        .Q(phy_tx_en), .C(clk_tx), .CE(1'b1),
        .D1(rgmii_txen_r), .D2(rgmii_txen_f),
        .R(~tx_rst_n), .S(1'b0));

endmodule
