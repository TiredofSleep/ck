/*
 * ck_eth_tx.v -- Pure PL RGMII Ethernet Transmitter
 *
 * Sends CK heartbeat data as UDP packets over PL Gigabit Ethernet.
 * No ARM, no PS. Pure fabric logic.
 *
 * PHY: RTL8211F-CG, RGMII interface, Bank 34, LVCMOS33
 * Board: Puzhi PZ7020-StarLite (XC7Z020-2CLG400I)
 *
 * Features:
 *   - MMCM: 50 MHz -> 125 MHz TX clock
 *   - RGMII DDR output via ODDR primitives
 *   - MDIO init sequence for RTL8211F RGMII timing
 *   - Fixed MAC/IP, broadcast UDP to port 7777
 *   - 10-byte payload per heartbeat tick
 *   - CRC-32 (IEEE 802.3) computed inline
 *
 * Packet structure (64 bytes minimum):
 *   Preamble(7) + SFD(1) + DstMAC(6) + SrcMAC(6) + EtherType(2) +
 *   IP Header(20) + UDP Header(8) + Payload(10) + Pad(8) + FCS(4)
 *
 * Payload format (10 bytes):
 *   tick_count[31:0]  (4 bytes, big-endian)
 *   phase_bc[3:0]     (upper nibble of byte 4)
 *   fuse_op[3:0]      (lower nibble of byte 4)
 *   coh_num[15:0]     (2 bytes, big-endian)
 *   coh_den[15:0]     (2 bytes, big-endian)
 *   bump[0]           (1 byte, LSB)
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
 */

module ck_eth_tx (
    input  wire        clk_50m,       // 50 MHz PL oscillator
    input  wire        rst_n,         // Active-low reset

    // Heartbeat inputs (50 MHz domain)
    input  wire        tick_done,     // One pulse per heartbeat tick
    input  wire [31:0] tick_count,
    input  wire [3:0]  phase_bc,
    input  wire [3:0]  fuse_op,
    input  wire [15:0] coh_num,
    input  wire [15:0] coh_den,
    input  wire        bump,

    // RGMII PHY interface
    output wire        phy_gtx_clk,   // 125 MHz DDR clock to PHY
    output wire [3:0]  phy_txd,       // 4-bit DDR data
    output wire        phy_tx_en,     // TX enable (DDR: EN on rising, ERR on falling)

    // MDIO management
    output wire        phy_mdc,       // Management clock
    inout  wire        phy_mdio,      // Management data (active-low for tristate)

    // Status
    output wire        mmcm_locked,   // MMCM lock indicator
    output wire        link_ready     // PHY init complete
);

    // =========================================================
    // MMCM: 50 MHz -> 125 MHz
    // VCO = 50 * 25 = 1250 MHz, CLKOUT0 = 1250 / 10 = 125 MHz
    // =========================================================

    wire clk_125;
    wire clk_fb;
    wire mmcm_lock_i;

    MMCME2_BASE #(
        .CLKIN1_PERIOD  (20.000),    // 50 MHz
        .CLKFBOUT_MULT_F(25.0),     // VCO = 1250 MHz
        .CLKOUT0_DIVIDE_F(10.0)     // 125 MHz
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
    // Synchronize tick_done from 50 MHz -> 125 MHz domain
    // =========================================================

    reg [2:0] td_sync;
    always @(posedge clk_tx or negedge tx_rst_n) begin
        if (!tx_rst_n)
            td_sync <= 3'b0;
        else
            td_sync <= {td_sync[1:0], tick_done};
    end
    wire td_rise = td_sync[1] & ~td_sync[2];

    // Latch heartbeat data on tick_done (50 MHz domain)
    reg [31:0] lat_tick;
    reg [3:0]  lat_phase, lat_fuse;
    reg [15:0] lat_coh_num, lat_coh_den;
    reg        lat_bump;

    always @(posedge clk_50m or negedge rst_n) begin
        if (!rst_n) begin
            lat_tick    <= 32'd0;
            lat_phase   <= 4'd0;
            lat_fuse    <= 4'd0;
            lat_coh_num <= 16'd0;
            lat_coh_den <= 16'd0;
            lat_bump    <= 1'b0;
        end else if (tick_done) begin
            lat_tick    <= tick_count;
            lat_phase   <= phase_bc;
            lat_fuse    <= fuse_op;
            lat_coh_num <= coh_num;
            lat_coh_den <= coh_den;
            lat_bump    <= bump;
        end
    end

    // Double-sync latched data to TX domain
    reg [31:0] tx_tick;
    reg [3:0]  tx_phase, tx_fuse;
    reg [15:0] tx_coh_num, tx_coh_den;
    reg        tx_bump;

    always @(posedge clk_tx) begin
        tx_tick    <= lat_tick;
        tx_phase   <= lat_phase;
        tx_fuse    <= lat_fuse;
        tx_coh_num <= lat_coh_num;
        tx_coh_den <= lat_coh_den;
        tx_bump    <= lat_bump;
    end

    // =========================================================
    // MDIO Controller -- Init RTL8211F for RGMII
    // =========================================================
    // RTL8211F needs register writes to enable RGMII TX/RX delay:
    //   1. Write page select register 31 = 0x0D08 (page 0xD08)
    //   2. Write register 17 bit[8]=1 (TX delay), bit[3]=1 (RX delay)
    //   3. Write page select register 31 = 0x0000 (back to page 0)
    //
    // MDIO frame: PRE(32x1) + ST(01) + OP(01=wr) + PHYAD(5) + REGAD(5) +
    //             TA(10) + DATA(16)
    //
    // MDC = 50 MHz / 128 ~ 390 kHz (well within 2.5 MHz max)

    localparam MDIO_PRE   = 32'hFFFF_FFFF;
    localparam PHY_ADDR   = 5'b00001;   // RTL8211F default address

    // MDIO write sequence (3 writes)
    localparam [2:0] MDIO_IDLE    = 3'd0,
                     MDIO_WRITE   = 3'd1,
                     MDIO_WAIT    = 3'd2,
                     MDIO_NEXT    = 3'd3,
                     MDIO_DONE    = 3'd4;

    // 3 register writes for RGMII delay config
    reg [4:0]  mdio_reg   [0:2];
    reg [15:0] mdio_data  [0:2];
    reg [1:0]  mdio_idx;

    initial begin
        // Write 1: Page select -> 0x0D08
        mdio_reg[0]  = 5'd31;
        mdio_data[0] = 16'h0D08;
        // Write 2: Reg 17 on page 0xD08 -> set TX delay (bit 8) + RX delay (bit 3)
        mdio_reg[1]  = 5'd17;
        mdio_data[1] = 16'h0108;  // bit[8]=1 TX delay, bit[3]=1 RX delay
        // Write 3: Page select -> 0x0000 (return to page 0)
        mdio_reg[2]  = 5'd31;
        mdio_data[2] = 16'h0000;
    end

    reg [2:0]  mdio_state;
    reg [6:0]  mdio_clk_div;   // /128 divider for MDC
    reg        mdio_clk_en;    // Pulse at MDC rate
    reg [5:0]  mdio_bit_cnt;   // Bit counter within frame
    reg [63:0] mdio_shift;     // Shift register for MDIO frame
    reg        mdio_oe;        // Output enable for MDIO
    reg        mdio_out;       // MDIO output bit
    reg [15:0] mdio_pause_cnt; // Pause between writes
    reg        mdio_init_done;

    assign phy_mdc  = mdio_clk_div[6];
    assign phy_mdio = mdio_oe ? mdio_out : 1'bz;
    assign link_ready = mdio_init_done;

    always @(posedge clk_50m or negedge rst_n) begin
        if (!rst_n) begin
            mdio_clk_div <= 7'd0;
            mdio_clk_en  <= 1'b0;
        end else begin
            mdio_clk_div <= mdio_clk_div + 7'd1;
            mdio_clk_en  <= (mdio_clk_div == 7'd63); // Pulse on rising edge of MDC
        end
    end

    always @(posedge clk_50m or negedge rst_n) begin
        if (!rst_n) begin
            mdio_state     <= MDIO_IDLE;
            mdio_idx       <= 2'd0;
            mdio_bit_cnt   <= 6'd0;
            mdio_shift     <= 64'd0;
            mdio_oe        <= 1'b0;
            mdio_out       <= 1'b1;
            mdio_pause_cnt <= 16'd0;
            mdio_init_done <= 1'b0;
        end else if (mdio_clk_en) begin
            case (mdio_state)
                MDIO_IDLE: begin
                    // Wait 50000 MDC clocks after reset (~128 ms) for PHY to boot
                    mdio_pause_cnt <= mdio_pause_cnt + 16'd1;
                    if (mdio_pause_cnt == 16'd50000) begin
                        mdio_state <= MDIO_WRITE;
                        mdio_bit_cnt <= 6'd0;
                        // Build MDIO write frame:
                        // PRE(32) + ST(2) + OP(2) + PHYAD(5) + REGAD(5) + TA(2) + DATA(16) = 64 bits
                        mdio_shift <= {MDIO_PRE, 2'b01, 2'b01, PHY_ADDR, mdio_reg[mdio_idx], 2'b10, mdio_data[mdio_idx]};
                        mdio_oe <= 1'b1;
                    end
                end

                MDIO_WRITE: begin
                    mdio_out <= mdio_shift[63];
                    mdio_shift <= {mdio_shift[62:0], 1'b1};
                    mdio_bit_cnt <= mdio_bit_cnt + 6'd1;
                    if (mdio_bit_cnt == 6'd63) begin
                        mdio_state <= MDIO_WAIT;
                        mdio_oe <= 1'b0;
                        mdio_out <= 1'b1;
                        mdio_pause_cnt <= 16'd0;
                    end
                end

                MDIO_WAIT: begin
                    // Pause between writes (64 MDC clocks)
                    mdio_pause_cnt <= mdio_pause_cnt + 16'd1;
                    if (mdio_pause_cnt == 16'd64) begin
                        mdio_state <= MDIO_NEXT;
                    end
                end

                MDIO_NEXT: begin
                    if (mdio_idx == 2'd2) begin
                        mdio_state <= MDIO_DONE;
                        mdio_init_done <= 1'b1;
                    end else begin
                        mdio_idx <= mdio_idx + 2'd1;
                        mdio_state <= MDIO_WRITE;
                        mdio_bit_cnt <= 6'd0;
                        mdio_shift <= {MDIO_PRE, 2'b01, 2'b01, PHY_ADDR,
                                       mdio_reg[mdio_idx + 2'd1], 2'b10,
                                       mdio_data[mdio_idx + 2'd1]};
                        mdio_oe <= 1'b1;
                    end
                end

                MDIO_DONE: begin
                    // Stay here. MDIO idle.
                    mdio_oe <= 1'b0;
                    mdio_out <= 1'b1;
                end
            endcase
        end
    end

    // =========================================================
    // Ethernet Frame Builder
    // =========================================================
    // Frame bytes stored in a shift buffer. Built on td_rise,
    // then clocked out via RGMII at 125 MHz DDR.
    //
    // Total frame (excluding preamble/SFD):
    //   DstMAC(6) + SrcMAC(6) + EtherType(2) + IP(20) + UDP(8) + Payload(10) + Pad(8) = 60 bytes
    //   + FCS(4) = 64 bytes
    //
    // With preamble: 7 + 1 + 64 = 72 bytes
    // IFG: 12 bytes minimum (96 bit times)

    localparam [47:0] DST_MAC = 48'hFFFF_FFFF_FFFF;  // Broadcast
    localparam [47:0] SRC_MAC = 48'h7E_C4_5A_00_77_77; // CK: 7E:C4:5A:00:77:77

    localparam [31:0] SRC_IP  = {8'd192, 8'd168, 8'd1, 8'd100};
    localparam [31:0] DST_IP  = {8'd192, 8'd168, 8'd1, 8'd255};
    localparam [15:0] SRC_PORT = 16'd7777;
    localparam [15:0] DST_PORT = 16'd7777;

    // State machine
    localparam [2:0] ST_IDLE     = 3'd0,
                     ST_BUILD    = 3'd1,
                     ST_CRC      = 3'd2,
                     ST_PREAMBLE = 3'd3,
                     ST_FRAME    = 3'd4,
                     ST_FCS      = 3'd5,
                     ST_IFG      = 3'd6;

    reg [2:0] tx_state;
    reg [7:0] frame_buf [0:59];  // 60 bytes (DstMAC through Pad, no FCS)
    reg [6:0] tx_byte_cnt;       // Byte counter
    reg [6:0] build_idx;         // Build index

    // CRC-32 (IEEE 802.3)
    reg [31:0] crc_reg;
    reg [31:0] crc_next;
    wire [7:0] crc_din;

    // RGMII output registers
    reg [3:0] rgmii_txd_r;  // Rising edge nibble
    reg [3:0] rgmii_txd_f;  // Falling edge nibble
    reg       rgmii_txen_r; // Rising edge TX_EN
    reg       rgmii_txen_f; // Falling edge TX_EN (TX_ERR, always 0)

    // IP header checksum (precomputed for fixed header)
    // IP header (20 bytes):
    //   Ver=4, IHL=5, TOS=0, TotalLen=38 (20+8+10),
    //   ID=0x0000, Flags=0x4000 (DF), TTL=64, Proto=17(UDP),
    //   Checksum=?, SrcIP, DstIP
    //
    // Checksum = ~(sum of 16-bit words excluding checksum field)
    // Pre-sum (fixed fields):
    //   0x4500 + 0x0026 + 0x0000 + 0x4000 + 0x4011 + SrcIP_hi + SrcIP_lo + DstIP_hi + DstIP_lo

    wire [31:0] ip_sum_raw = 32'h4500 + 32'h0026 + 32'h0000 + 32'h4000 + 32'h4011 +
                             {16'd0, SRC_IP[31:16]} + {16'd0, SRC_IP[15:0]} +
                             {16'd0, DST_IP[31:16]} + {16'd0, DST_IP[15:0]};
    wire [15:0] ip_sum_folded = ip_sum_raw[15:0] + ip_sum_raw[31:16];
    wire [15:0] ip_checksum = ~(ip_sum_folded + {15'd0, ip_sum_folded[15] & 1'b0});
    // Proper fold: may need second carry
    wire [16:0] ip_fold1 = {1'b0, ip_sum_raw[15:0]} + {1'b0, ip_sum_raw[31:16]};
    wire [16:0] ip_fold2 = {1'b0, ip_fold1[15:0]} + {16'd0, ip_fold1[16]};
    wire [15:0] ip_cksum = ~ip_fold2[15:0];

    // UDP length = 8 header + 10 payload = 18
    localparam [15:0] UDP_LEN = 16'd18;
    // IP total length = 20 + 18 = 38
    localparam [15:0] IP_TOTAL_LEN = 16'd38;

    // Build frame buffer on td_rise
    integer i;
    always @(posedge clk_tx or negedge tx_rst_n) begin
        if (!tx_rst_n) begin
            tx_state    <= ST_IDLE;
            tx_byte_cnt <= 7'd0;
            build_idx   <= 7'd0;
            crc_reg     <= 32'hFFFF_FFFF;
            rgmii_txd_r <= 4'd0;
            rgmii_txd_f <= 4'd0;
            rgmii_txen_r <= 1'b0;
            rgmii_txen_f <= 1'b0;
        end else begin
            case (tx_state)

            ST_IDLE: begin
                rgmii_txen_r <= 1'b0;
                rgmii_txen_f <= 1'b0;
                rgmii_txd_r  <= 4'd0;
                rgmii_txd_f  <= 4'd0;
                if (td_rise && mdio_init_done) begin
                    tx_state <= ST_BUILD;
                    build_idx <= 7'd0;
                end
            end

            ST_BUILD: begin
                // Build 60-byte frame in frame_buf
                // Destination MAC (bytes 0-5)
                frame_buf[0]  <= DST_MAC[47:40];
                frame_buf[1]  <= DST_MAC[39:32];
                frame_buf[2]  <= DST_MAC[31:24];
                frame_buf[3]  <= DST_MAC[23:16];
                frame_buf[4]  <= DST_MAC[15:8];
                frame_buf[5]  <= DST_MAC[7:0];
                // Source MAC (bytes 6-11)
                frame_buf[6]  <= SRC_MAC[47:40];
                frame_buf[7]  <= SRC_MAC[39:32];
                frame_buf[8]  <= SRC_MAC[31:24];
                frame_buf[9]  <= SRC_MAC[23:16];
                frame_buf[10] <= SRC_MAC[15:8];
                frame_buf[11] <= SRC_MAC[7:0];
                // EtherType: IPv4 = 0x0800 (bytes 12-13)
                frame_buf[12] <= 8'h08;
                frame_buf[13] <= 8'h00;
                // IP Header (bytes 14-33)
                frame_buf[14] <= 8'h45;              // Version=4, IHL=5
                frame_buf[15] <= 8'h00;              // TOS
                frame_buf[16] <= IP_TOTAL_LEN[15:8]; // Total Length
                frame_buf[17] <= IP_TOTAL_LEN[7:0];
                frame_buf[18] <= 8'h00;              // ID
                frame_buf[19] <= 8'h00;
                frame_buf[20] <= 8'h40;              // Flags: DF
                frame_buf[21] <= 8'h00;              // Fragment Offset
                frame_buf[22] <= 8'h40;              // TTL=64
                frame_buf[23] <= 8'h11;              // Protocol=UDP
                frame_buf[24] <= ip_cksum[15:8];     // Header Checksum
                frame_buf[25] <= ip_cksum[7:0];
                frame_buf[26] <= SRC_IP[31:24];      // Source IP
                frame_buf[27] <= SRC_IP[23:16];
                frame_buf[28] <= SRC_IP[15:8];
                frame_buf[29] <= SRC_IP[7:0];
                frame_buf[30] <= DST_IP[31:24];      // Dest IP
                frame_buf[31] <= DST_IP[23:16];
                frame_buf[32] <= DST_IP[15:8];
                frame_buf[33] <= DST_IP[7:0];
                // UDP Header (bytes 34-41)
                frame_buf[34] <= SRC_PORT[15:8];
                frame_buf[35] <= SRC_PORT[7:0];
                frame_buf[36] <= DST_PORT[15:8];
                frame_buf[37] <= DST_PORT[7:0];
                frame_buf[38] <= UDP_LEN[15:8];
                frame_buf[39] <= UDP_LEN[7:0];
                frame_buf[40] <= 8'h00;              // UDP Checksum (0 = disabled)
                frame_buf[41] <= 8'h00;
                // Payload (bytes 42-51): 10 bytes
                frame_buf[42] <= tx_tick[31:24];
                frame_buf[43] <= tx_tick[23:16];
                frame_buf[44] <= tx_tick[15:8];
                frame_buf[45] <= tx_tick[7:0];
                frame_buf[46] <= {tx_phase, tx_fuse};
                frame_buf[47] <= tx_coh_num[15:8];
                frame_buf[48] <= tx_coh_num[7:0];
                frame_buf[49] <= tx_coh_den[15:8];
                frame_buf[50] <= tx_coh_den[7:0];
                frame_buf[51] <= {7'd0, tx_bump};
                // Pad to 60 bytes minimum (bytes 52-59)
                frame_buf[52] <= 8'h00;
                frame_buf[53] <= 8'h00;
                frame_buf[54] <= 8'h00;
                frame_buf[55] <= 8'h00;
                frame_buf[56] <= 8'h00;
                frame_buf[57] <= 8'h00;
                frame_buf[58] <= 8'h00;
                frame_buf[59] <= 8'h00;

                tx_state <= ST_CRC;
                tx_byte_cnt <= 7'd0;
                crc_reg <= 32'hFFFF_FFFF;
            end

            ST_CRC: begin
                // Compute CRC-32 over frame_buf[0..59]
                if (tx_byte_cnt < 7'd60) begin
                    crc_reg <= crc32_byte(crc_reg, frame_buf[tx_byte_cnt]);
                    tx_byte_cnt <= tx_byte_cnt + 7'd1;
                end else begin
                    tx_state <= ST_PREAMBLE;
                    tx_byte_cnt <= 7'd0;
                end
            end

            ST_PREAMBLE: begin
                // 7 bytes of 0x55 preamble + 1 byte 0xD5 SFD = 8 bytes
                // Each byte = 2 RGMII clocks (4 bits per edge)
                rgmii_txen_r <= 1'b1;
                rgmii_txen_f <= 1'b0; // TX_ERR = 0
                if (tx_byte_cnt < 7'd7) begin
                    rgmii_txd_r <= 4'h5;  // Preamble low nibble
                    rgmii_txd_f <= 4'h5;  // Preamble high nibble
                    tx_byte_cnt <= tx_byte_cnt + 7'd1;
                end else if (tx_byte_cnt == 7'd7) begin
                    rgmii_txd_r <= 4'h5;  // SFD low nibble: 0xD5
                    rgmii_txd_f <= 4'hD;  // SFD high nibble
                    tx_byte_cnt <= 7'd0;
                    tx_state <= ST_FRAME;
                end
            end

            ST_FRAME: begin
                // Clock out frame_buf[0..59], one byte per clock
                // Rising edge = low nibble, falling edge = high nibble
                rgmii_txen_r <= 1'b1;
                rgmii_txen_f <= 1'b0;
                rgmii_txd_r <= frame_buf[tx_byte_cnt][3:0];
                rgmii_txd_f <= frame_buf[tx_byte_cnt][7:4];
                tx_byte_cnt <= tx_byte_cnt + 7'd1;
                if (tx_byte_cnt == 7'd59) begin
                    tx_state <= ST_FCS;
                    tx_byte_cnt <= 7'd0;
                end
            end

            ST_FCS: begin
                // Clock out 4-byte FCS (CRC complement, LSB first per byte, bytes in order)
                rgmii_txen_r <= 1'b1;
                rgmii_txen_f <= 1'b0;
                case (tx_byte_cnt[1:0])
                    2'd0: begin
                        rgmii_txd_r <= ~crc_reg[3:0];   // CRC byte 0 low nibble
                        rgmii_txd_f <= ~crc_reg[7:4];   // CRC byte 0 high nibble
                    end
                    2'd1: begin
                        rgmii_txd_r <= ~crc_reg[11:8];
                        rgmii_txd_f <= ~crc_reg[15:12];
                    end
                    2'd2: begin
                        rgmii_txd_r <= ~crc_reg[19:16];
                        rgmii_txd_f <= ~crc_reg[23:20];
                    end
                    2'd3: begin
                        rgmii_txd_r <= ~crc_reg[27:24];
                        rgmii_txd_f <= ~crc_reg[31:28];
                    end
                endcase
                tx_byte_cnt <= tx_byte_cnt + 7'd1;
                if (tx_byte_cnt == 7'd3) begin
                    tx_state <= ST_IFG;
                    tx_byte_cnt <= 7'd0;
                end
            end

            ST_IFG: begin
                // Inter-frame gap: 12 bytes (96 bit times at gigabit)
                rgmii_txen_r <= 1'b0;
                rgmii_txen_f <= 1'b0;
                rgmii_txd_r  <= 4'd0;
                rgmii_txd_f  <= 4'd0;
                tx_byte_cnt <= tx_byte_cnt + 7'd1;
                if (tx_byte_cnt == 7'd11) begin
                    tx_state <= ST_IDLE;
                end
            end

            endcase
        end
    end

    // =========================================================
    // CRC-32 Function (IEEE 802.3 polynomial)
    // =========================================================
    // Polynomial: 0x04C11DB7 (bit-reversed: 0xEDB88320)
    // Process one byte at a time, LSB first

    function [31:0] crc32_byte;
        input [31:0] crc_in;
        input [7:0]  data_in;
        reg [31:0] c;
        reg [7:0]  d;
        integer j;
        begin
            c = crc_in;
            d = data_in;
            for (j = 0; j < 8; j = j + 1) begin
                if ((c[0] ^ d[0]) == 1'b1)
                    c = {1'b0, c[31:1]} ^ 32'hEDB88320;
                else
                    c = {1'b0, c[31:1]};
                d = {1'b0, d[7:1]};
            end
            crc32_byte = c;
        end
    endfunction

    // =========================================================
    // RGMII ODDR Output Primitives
    // =========================================================
    // RGMII spec: data changes on both edges of GTX_CLK
    // Use ODDR to output DDR data aligned with clock

    // GTX_CLK: 125 MHz clock to PHY (DDR: 1 on rising, 0 on falling)
    ODDR #(
        .DDR_CLK_EDGE("SAME_EDGE"),
        .INIT(1'b0),
        .SRTYPE("ASYNC")
    ) oddr_gtx_clk (
        .Q(phy_gtx_clk),
        .C(clk_tx),
        .CE(1'b1),
        .D1(1'b1),
        .D2(1'b0),
        .R(~tx_rst_n),
        .S(1'b0)
    );

    // TXD[3:0] DDR outputs
    genvar gi;
    generate
        for (gi = 0; gi < 4; gi = gi + 1) begin : gen_txd_oddr
            ODDR #(
                .DDR_CLK_EDGE("SAME_EDGE"),
                .INIT(1'b0),
                .SRTYPE("ASYNC")
            ) oddr_txd (
                .Q(phy_txd[gi]),
                .C(clk_tx),
                .CE(1'b1),
                .D1(rgmii_txd_r[gi]),
                .D2(rgmii_txd_f[gi]),
                .R(~tx_rst_n),
                .S(1'b0)
            );
        end
    endgenerate

    // TX_EN DDR output (rising = TX_EN, falling = TX_ERR)
    ODDR #(
        .DDR_CLK_EDGE("SAME_EDGE"),
        .INIT(1'b0),
        .SRTYPE("ASYNC")
    ) oddr_tx_en (
        .Q(phy_tx_en),
        .C(clk_tx),
        .CE(1'b1),
        .D1(rgmii_txen_r),
        .D2(rgmii_txen_f),
        .R(~tx_rst_n),
        .S(1'b0)
    );

endmodule
