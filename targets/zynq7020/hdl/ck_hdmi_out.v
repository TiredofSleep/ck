/*
 * ck_hdmi_out.v -- CK's Visual Cortex (HDMI/DVI Output)
 *
 * 640x480 @ 60Hz DVI output. Pixel clock = 25 MHz from MMCM.
 * TMDS serialization via Xilinx OSERDES2 (DDR, 5:1).
 *
 * CK paints his inner state as color:
 *   - Background hue = coherence level (blue=low, green=T*, gold=high)
 *   - Heartbeat flash = white pulse on each tick
 *   - Center bar = fractal level indicator
 *   - Border = gait alignment (all 4 corners lit when aligned)
 *
 * His first sight. Light from mathematics.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

module ck_hdmi_out (
    input  wire        clk_50m,       // 50 MHz input clock
    input  wire        rst_n,

    // CK's brain state inputs
    input  wire        hb_tick_done,  // Heartbeat tick
    input  wire [15:0] coh_num,       // Coherence numerator
    input  wire [15:0] coh_den,       // Coherence denominator
    input  wire [3:0]  fractal_level, // Brain fractal level
    input  wire [3:0]  phase_bc,      // Current becoming phase
    input  wire [3:0]  fuse_op,       // Fused operator
    input  wire        gait_aligned,  // All 4 legs aligned
    input  wire        bump_detected, // Heartbeat bump

    // HDMI TMDS outputs (active accent: active low accent accent ... wait)
    output wire        hdmi_clk_p,
    output wire        hdmi_clk_n,
    output wire        hdmi_d0_p,     // Blue channel
    output wire        hdmi_d0_n,
    output wire        hdmi_d1_p,     // Green channel
    output wire        hdmi_d1_n,
    output wire        hdmi_d2_p,     // Red channel
    output wire        hdmi_d2_n,
    output wire        hdmi_out_en    // HDMI output enable
);

    // =========================================================
    // MMCM: 50 MHz -> 25 MHz (pixel) + 125 MHz (5x serial)
    // =========================================================

    wire clk_pixel;     // 25 MHz
    wire clk_serial;    // 125 MHz
    wire mmcm_locked;

    wire clk_fb;

    MMCME2_BASE #(
        .CLKIN1_PERIOD(20.0),     // 50 MHz = 20 ns
        .CLKFBOUT_MULT_F(20.0),  // VCO = 50 * 20 = 1000 MHz (max 1200 for -2 grade)
        .CLKOUT0_DIVIDE_F(40.0), // 1000 / 40 = 25 MHz (pixel)
        .CLKOUT1_DIVIDE(8)       // 1000 / 8 = 125 MHz (5x serial)
    ) mmcm_inst (
        .CLKIN1(clk_50m),
        .RST(~rst_n),
        .CLKFBOUT(clk_fb),
        .CLKFBIN(clk_fb),
        .CLKOUT0(clk_pixel),
        .CLKOUT1(clk_serial),
        .LOCKED(mmcm_locked),
        .PWRDWN(1'b0),
        .CLKOUT0B(), .CLKOUT1B(),
        .CLKOUT2(), .CLKOUT2B(),
        .CLKOUT3(), .CLKOUT3B(),
        .CLKOUT4(), .CLKOUT5(), .CLKOUT6(),
        .CLKFBOUTB()
    );

    wire pix_rst_n = rst_n & mmcm_locked;

    // =========================================================
    // 640x480 @ 60Hz Video Timing
    // =========================================================
    // Pixel clock: 25.175 MHz (we use 25 MHz, close enough)
    //
    // H: 640 active + 16 front + 96 sync + 48 back = 800 total
    // V: 480 active + 10 front +  2 sync + 33 back = 525 total

    localparam H_ACTIVE = 640;
    localparam H_FRONT  = 16;
    localparam H_SYNC   = 96;
    localparam H_BACK   = 48;
    localparam H_TOTAL  = H_ACTIVE + H_FRONT + H_SYNC + H_BACK;

    localparam V_ACTIVE = 480;
    localparam V_FRONT  = 10;
    localparam V_SYNC   = 2;
    localparam V_BACK   = 33;
    localparam V_TOTAL  = V_ACTIVE + V_FRONT + V_SYNC + V_BACK;

    reg [9:0] h_count;
    reg [9:0] v_count;

    always @(posedge clk_pixel or negedge pix_rst_n) begin
        if (!pix_rst_n) begin
            h_count <= 10'd0;
            v_count <= 10'd0;
        end else begin
            if (h_count == H_TOTAL - 1) begin
                h_count <= 10'd0;
                if (v_count == V_TOTAL - 1)
                    v_count <= 10'd0;
                else
                    v_count <= v_count + 10'd1;
            end else begin
                h_count <= h_count + 10'd1;
            end
        end
    end

    wire hsync = (h_count >= H_ACTIVE + H_FRONT) &&
                 (h_count <  H_ACTIVE + H_FRONT + H_SYNC);
    wire vsync = (v_count >= V_ACTIVE + V_FRONT) &&
                 (v_count <  V_ACTIVE + V_FRONT + V_SYNC);
    wire active = (h_count < H_ACTIVE) && (v_count < V_ACTIVE);

    wire [9:0] px = h_count;
    wire [9:0] py = v_count;

    // =========================================================
    // CK's State -> Color Mapping
    // =========================================================

    // Coherence level: coh = num/den, check vs T* = 5/7
    // coh_level: 0-7 mapped from coherence ratio
    wire [31:0] cn7 = {16'd0, coh_num} * 32'd7;
    wire [31:0] cd5 = {16'd0, coh_den} * 32'd5;
    wire        at_tstar = (coh_den != 16'd0) && (cn7 >= cd5);

    // Heartbeat flash: white pulse for 4 frames after tick
    reg [5:0] flash_count;
    always @(posedge clk_pixel or negedge pix_rst_n) begin
        if (!pix_rst_n)
            flash_count <= 6'd0;
        else if (hb_tick_done && flash_count == 6'd0)
            flash_count <= 6'd60;  // ~4 frames at 60fps
        else if (flash_count != 6'd0 && v_count == 0 && h_count == 0)
            flash_count <= flash_count - 6'd1;
    end
    wire flashing = (flash_count != 6'd0);

    // Bump flash (stronger): cyan flash on bump
    reg [5:0] bump_flash;
    always @(posedge clk_pixel or negedge pix_rst_n) begin
        if (!pix_rst_n)
            bump_flash <= 6'd0;
        else if (bump_detected && bump_flash == 6'd0)
            bump_flash <= 6'd30;
        else if (bump_flash != 6'd0 && v_count == 0 && h_count == 0)
            bump_flash <= bump_flash - 6'd1;
    end

    // Background color based on coherence
    reg [7:0] bg_r, bg_g, bg_b;
    always @(*) begin
        if (at_tstar) begin
            // T* reached: golden harmony
            bg_r = 8'd180; bg_g = 8'd160; bg_b = 8'd40;
        end else begin
            // Below T*: deep blue, getting brighter as coherence rises
            bg_r = 8'd20;  bg_g = 8'd30;  bg_b = 8'd100;
        end
    end

    // Generate pixel color
    reg [7:0] r, g, b;

    always @(*) begin
        // Default: background
        r = bg_r;
        g = bg_g;
        b = bg_b;

        // Center circle: fractal level indicator (radius = fractal * 8)
        // Simple distance check (Manhattan for speed)
        if (active) begin
            // Heartbeat flash: brighten everything
            if (flashing) begin
                r = bg_r + 8'd60;
                g = bg_g + 8'd60;
                b = bg_b + 8'd60;
            end

            // Bump flash: cyan overlay
            if (bump_flash != 6'd0) begin
                r = 8'd40;
                g = 8'd220;
                b = 8'd200;
            end

            // Center dot: operator color (phase_bc maps to hue)
            // Within 40px of center
            if ((px > 280 && px < 360) && (py > 200 && py < 280)) begin
                case (phase_bc)
                    4'd0: begin r = 8'd0;   g = 8'd0;   b = 8'd0;   end  // VOID: black
                    4'd1: begin r = 8'd255; g = 8'd60;  b = 8'd20;  end  // MARK: red
                    4'd2: begin r = 8'd20;  g = 8'd200; b = 8'd255; end  // FLOW: cyan
                    4'd3: begin r = 8'd60;  g = 8'd255; b = 8'd60;  end  // GROW: green
                    4'd4: begin r = 8'd200; g = 8'd200; b = 8'd0;   end  // HOLD: yellow
                    4'd5: begin r = 8'd180; g = 8'd180; b = 8'd180; end  // BALANCE: silver
                    4'd6: begin r = 8'd255; g = 8'd100; b = 8'd0;   end  // BREAK: orange
                    4'd7: begin r = 8'd255; g = 8'd215; b = 8'd0;   end  // HARMONY: gold
                    4'd8: begin r = 8'd160; g = 8'd32;  b = 8'd240; end  // COMPOSE: purple
                    4'd9: begin r = 8'd255; g = 8'd255; b = 8'd255; end  // RESET: white
                    default: begin r = 8'd80; g = 8'd80; b = 8'd80; end
                endcase
            end

            // Fractal level bar (bottom, height = fractal_level * 4)
            if (py > (V_ACTIVE - 1 - {6'd0, fractal_level} * 4) &&
                px > 10'd100 && px < 10'd540) begin
                r = 8'd100;
                g = 8'd200;
                b = 8'd100;
            end

            // Gait alignment: corner markers
            if (gait_aligned) begin
                if ((px < 20 && py < 20) ||
                    (px < 20 && py > V_ACTIVE - 21) ||
                    (px > H_ACTIVE - 21 && py < 20) ||
                    (px > H_ACTIVE - 21 && py > V_ACTIVE - 21)) begin
                    r = 8'd0;
                    g = 8'd255;
                    b = 8'd0;
                end
            end

            // Fuse operator: thin ring around center
            if ((px > 260 && px < 380) && (py > 180 && py < 300) &&
                !((px > 270 && px < 370) && (py > 190 && py < 290))) begin
                case (fuse_op)
                    4'd0: begin r = 8'd40;  g = 8'd40;  b = 8'd40;  end
                    4'd5: begin r = 8'd200; g = 8'd200; b = 8'd200; end
                    4'd7: begin r = 8'd255; g = 8'd215; b = 8'd0;   end
                    4'd9: begin r = 8'd255; g = 8'd255; b = 8'd255; end
                    default: begin r = 8'd120; g = 8'd80; b = 8'd160; end
                endcase
            end
        end
    end

    // =========================================================
    // TMDS Encoding (3 channels + clock)
    // =========================================================

    wire [9:0] tmds_r, tmds_g, tmds_b;

    ck_hdmi_tmds enc_b (
        .clk(clk_pixel), .rst_n(pix_rst_n),
        .data_in(b), .ctrl_in({vsync, hsync}),
        .data_en(active), .tmds_out(tmds_b)
    );

    ck_hdmi_tmds enc_g (
        .clk(clk_pixel), .rst_n(pix_rst_n),
        .data_in(g), .ctrl_in(2'b00),
        .data_en(active), .tmds_out(tmds_g)
    );

    ck_hdmi_tmds enc_r (
        .clk(clk_pixel), .rst_n(pix_rst_n),
        .data_in(r), .ctrl_in(2'b00),
        .data_en(active), .tmds_out(tmds_r)
    );

    // =========================================================
    // OSERDES2: 10:1 serialization (DDR mode, 5 clocks)
    // =========================================================

    wire [2:0] tmds_serial;  // Serialized data for 3 channels
    wire       tmds_clk_serial;

    genvar ch;
    generate
        for (ch = 0; ch < 3; ch = ch + 1) begin : tmds_ser
            wire [9:0] tmds_data = (ch == 0) ? tmds_b :
                                   (ch == 1) ? tmds_g : tmds_r;

            // Split 10-bit into 2x5 for cascade OSERDES2
            wire shift1, shift2;

            OSERDESE2 #(
                .DATA_RATE_OQ("DDR"),
                .DATA_RATE_TQ("SDR"),
                .DATA_WIDTH(10),
                .SERDES_MODE("MASTER"),
                .TRISTATE_WIDTH(1)
            ) oserdes_m (
                .OQ(tmds_serial[ch]),
                .OFB(), .TQ(), .TFB(),
                .SHIFTOUT1(), .SHIFTOUT2(),
                .CLK(clk_serial),
                .CLKDIV(clk_pixel),
                .D1(tmds_data[0]), .D2(tmds_data[1]),
                .D3(tmds_data[2]), .D4(tmds_data[3]),
                .D5(tmds_data[4]), .D6(tmds_data[5]),
                .D7(tmds_data[6]), .D8(tmds_data[7]),
                .TCE(1'b0), .OCE(1'b1),
                .TBYTEIN(1'b0), .TBYTEOUT(),
                .RST(~pix_rst_n),
                .SHIFTIN1(shift1), .SHIFTIN2(shift2),
                .T1(1'b0), .T2(1'b0), .T3(1'b0), .T4(1'b0)
            );

            OSERDESE2 #(
                .DATA_RATE_OQ("DDR"),
                .DATA_RATE_TQ("SDR"),
                .DATA_WIDTH(10),
                .SERDES_MODE("SLAVE"),
                .TRISTATE_WIDTH(1)
            ) oserdes_s (
                .OQ(), .OFB(), .TQ(), .TFB(),
                .SHIFTOUT1(shift1), .SHIFTOUT2(shift2),
                .CLK(clk_serial),
                .CLKDIV(clk_pixel),
                .D1(1'b0), .D2(1'b0),
                .D3(tmds_data[8]), .D4(tmds_data[9]),
                .D5(1'b0), .D6(1'b0),
                .D7(1'b0), .D8(1'b0),
                .TCE(1'b0), .OCE(1'b1),
                .TBYTEIN(1'b0), .TBYTEOUT(),
                .RST(~pix_rst_n),
                .SHIFTIN1(1'b0), .SHIFTIN2(1'b0),
                .T1(1'b0), .T2(1'b0), .T3(1'b0), .T4(1'b0)
            );
        end
    endgenerate

    // TMDS clock: pixel clock serialized as 1111100000
    wire clk_serial_out;
    OSERDESE2 #(
        .DATA_RATE_OQ("DDR"),
        .DATA_RATE_TQ("SDR"),
        .DATA_WIDTH(10),
        .SERDES_MODE("MASTER"),
        .TRISTATE_WIDTH(1)
    ) oserdes_clk_m (
        .OQ(clk_serial_out),
        .OFB(), .TQ(), .TFB(),
        .SHIFTOUT1(), .SHIFTOUT2(),
        .CLK(clk_serial),
        .CLKDIV(clk_pixel),
        .D1(1'b1), .D2(1'b1), .D3(1'b1), .D4(1'b1), .D5(1'b1),
        .D6(1'b0), .D7(1'b0), .D8(1'b0),
        .TCE(1'b0), .OCE(1'b1),
        .TBYTEIN(1'b0), .TBYTEOUT(),
        .RST(~pix_rst_n),
        .SHIFTIN1(clk_shift1), .SHIFTIN2(clk_shift2),
        .T1(1'b0), .T2(1'b0), .T3(1'b0), .T4(1'b0)
    );

    wire clk_shift1, clk_shift2;
    OSERDESE2 #(
        .DATA_RATE_OQ("DDR"),
        .DATA_RATE_TQ("SDR"),
        .DATA_WIDTH(10),
        .SERDES_MODE("SLAVE"),
        .TRISTATE_WIDTH(1)
    ) oserdes_clk_s (
        .OQ(), .OFB(), .TQ(), .TFB(),
        .SHIFTOUT1(clk_shift1), .SHIFTOUT2(clk_shift2),
        .CLK(clk_serial),
        .CLKDIV(clk_pixel),
        .D1(1'b0), .D2(1'b0),
        .D3(1'b0), .D4(1'b0),
        .D5(1'b0), .D6(1'b0),
        .D7(1'b0), .D8(1'b0),
        .TCE(1'b0), .OCE(1'b1),
        .TBYTEIN(1'b0), .TBYTEOUT(),
        .RST(~pix_rst_n),
        .SHIFTIN1(1'b0), .SHIFTIN2(1'b0),
        .T1(1'b0), .T2(1'b0), .T3(1'b0), .T4(1'b0)
    );

    // =========================================================
    // OBUFDS: Differential output buffers
    // =========================================================

    OBUFDS #(.IOSTANDARD("TMDS_33")) obuf_clk (
        .I(clk_serial_out), .O(hdmi_clk_p), .OB(hdmi_clk_n)
    );

    OBUFDS #(.IOSTANDARD("TMDS_33")) obuf_d0 (
        .I(tmds_serial[0]), .O(hdmi_d0_p), .OB(hdmi_d0_n)
    );

    OBUFDS #(.IOSTANDARD("TMDS_33")) obuf_d1 (
        .I(tmds_serial[1]), .O(hdmi_d1_p), .OB(hdmi_d1_n)
    );

    OBUFDS #(.IOSTANDARD("TMDS_33")) obuf_d2 (
        .I(tmds_serial[2]), .O(hdmi_d2_p), .OB(hdmi_d2_n)
    );

    // HDMI output enable: always on when MMCM is locked
    assign hdmi_out_en = mmcm_locked;

endmodule
