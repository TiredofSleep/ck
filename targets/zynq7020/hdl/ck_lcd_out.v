/*
 * ck_lcd_out.v -- Parallel RGB LCD Output for CK
 *
 * Drives a 480x272 TFT LCD (PZ-LCD430, AT043TN24 or compatible)
 * via 24-bit parallel RGB interface on the 40P expansion connector.
 *
 * CK's internal state maps to color:
 *   - Background: warm gold when coherent (T* = 5/7), deep blue when below
 *   - Heartbeat flash: white pulse on each tick
 *   - Center dot: operator hue (phase_bc mapped to 10 TIG colors)
 *   - Fractal bar: bottom strip shows fractal level
 *   - Gait marks: green corners when legs aligned
 *   - Fuse ring: colored annulus around center dot
 *
 * MMCM: 50 MHz -> 9 MHz pixel clock (within AT043TN24 range 6-12 MHz)
 * Timing: 480x272 active, 532x298 total, ~56.8 Hz refresh
 *
 * This gives CK a face. His coherence becomes light.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

module ck_lcd_out (
    input  wire        clk_50m,       // 50 MHz system clock
    input  wire        rst_n,

    // CK brain state inputs
    input  wire [3:0]  phase_bc,      // Current Becoming phase (operator)
    input  wire [3:0]  fuse_op,       // Fused operator
    input  wire [15:0] coh_num,       // Coherence numerator
    input  wire [15:0] coh_den,       // Coherence denominator
    input  wire        hb_tick,       // Heartbeat tick pulse
    input  wire [3:0]  fractal_level, // Brain fractal depth
    input  wire        gait_aligned,  // All gait legs aligned
    input  wire [31:0] tick_count,    // Heartbeat tick counter

    // LCD parallel RGB outputs
    output wire [7:0]  lcd_r,         // Red data
    output wire [7:0]  lcd_g,         // Green data
    output wire [7:0]  lcd_b,         // Blue data
    output wire        lcd_dclk,      // Pixel clock to LCD
    output wire        lcd_hsync,     // Horizontal sync (directly active-low for most panels)
    output wire        lcd_vsync,     // Vertical sync
    output wire        lcd_de,        // Data enable (active = pixel valid)
    output wire        lcd_bl,        // Backlight enable (active high)

    // Diagnostic
    output wire        lcd_mmcm_locked // MMCM lock status for debug
);

    // =========================================================
    // Parameters: AT043TN24 / 480x272 LCD Timing
    // =========================================================

    // Horizontal timing (pixels)
    localparam H_ACTIVE  = 11'd480;
    localparam H_FP      = 11'd8;      // Front porch
    localparam H_SYNC    = 11'd1;      // Sync pulse width
    localparam H_BP      = 11'd43;     // Back porch
    localparam H_TOTAL   = H_ACTIVE + H_FP + H_SYNC + H_BP; // 532

    // Vertical timing (lines)
    localparam V_ACTIVE  = 10'd272;
    localparam V_FP      = 10'd4;
    localparam V_SYNC    = 10'd10;
    localparam V_BP      = 10'd12;
    localparam V_TOTAL   = V_ACTIVE + V_FP + V_SYNC + V_BP;  // 298

    // =========================================================
    // MMCM: 50 MHz -> 9 MHz Pixel Clock
    // =========================================================
    // VCO = 50 * 18 = 900 MHz (within 600-1200 range)
    // CLKOUT0 = 900 / 100 = 9 MHz

    wire pclk;          // 9 MHz pixel clock
    wire pclk_locked;
    wire clk_fb;

    MMCME2_BASE #(
        .CLKIN1_PERIOD   (20.000),    // 50 MHz input
        .CLKFBOUT_MULT_F (18.0),      // VCO = 900 MHz
        .CLKOUT0_DIVIDE_F(18.0),      // 900/18 = 50 MHz (safe default, not used)
        .CLKOUT1_DIVIDE  (100)        // 900/100 = 9 MHz pixel clock (integer)
    ) mmcm_lcd (
        .CLKIN1   (clk_50m),
        .CLKFBIN  (clk_fb),
        .CLKFBOUT (clk_fb),
        .CLKOUT0  (),
        .CLKOUT1  (pclk),             // 9 MHz pixel clock on CLKOUT1
        .LOCKED   (pclk_locked),
        .PWRDWN   (1'b0),
        .RST      (~rst_n)
    );

    // Internal reset: wait for MMCM lock
    wire int_rst_n = rst_n & pclk_locked;

    // =========================================================
    // LCD DCLK output (fabric, not ODDR)
    // =========================================================
    // ODDR removed: pin probe mode routes lcd_dclk through a
    // config MUX, which ODDR cannot legally drive. Instead we
    // pass the 9 MHz pclk through fabric. At 9 MHz the extra
    // routing delay is negligible for the AT043TN24 panel.

    assign lcd_dclk = pclk;

    // Backlight: always on when locked
    assign lcd_bl = pclk_locked;

    // =========================================================
    // Horizontal and Vertical Counters
    // =========================================================

    reg [10:0] h_cnt;
    reg [9:0]  v_cnt;

    always @(posedge pclk or negedge int_rst_n) begin
        if (!int_rst_n) begin
            h_cnt <= 11'd0;
            v_cnt <= 10'd0;
        end else begin
            if (h_cnt == H_TOTAL - 1) begin
                h_cnt <= 11'd0;
                if (v_cnt == V_TOTAL - 1)
                    v_cnt <= 10'd0;
                else
                    v_cnt <= v_cnt + 10'd1;
            end else begin
                h_cnt <= h_cnt + 11'd1;
            end
        end
    end

    // Sync signals (active low for most TFT panels)
    // Sync pulse is at the END after front porch
    wire h_sync_zone = (h_cnt >= H_ACTIVE + H_FP) &&
                       (h_cnt <  H_ACTIVE + H_FP + H_SYNC);
    wire v_sync_zone = (v_cnt >= V_ACTIVE + V_FP) &&
                       (v_cnt <  V_ACTIVE + V_FP + V_SYNC);

    assign lcd_hsync = ~h_sync_zone;
    assign lcd_vsync = ~v_sync_zone;

    // Data enable: high during active video
    wire active = (h_cnt < H_ACTIVE) && (v_cnt < V_ACTIVE);
    assign lcd_de = active;

    // Pixel coordinates (only valid during active)
    wire [10:0] px = h_cnt;
    wire [9:0]  py = v_cnt;

    // =========================================================
    // Coherence Check: T* = 5/7
    // =========================================================

    wire [31:0] cn7 = {16'd0, coh_num} * 32'd7;
    wire [31:0] cd5 = {16'd0, coh_den} * 32'd5;
    wire coherent = (coh_den != 16'd0) && (cn7 >= cd5);

    // =========================================================
    // Heartbeat Flash Timer (white pulse lasting ~8 frames)
    // =========================================================

    reg [7:0] flash_timer;
    always @(posedge pclk or negedge int_rst_n) begin
        if (!int_rst_n)
            flash_timer <= 8'd0;
        else if (hb_tick)
            flash_timer <= 8'd255;
        else if (flash_timer != 0 && h_cnt == 0 && v_cnt == 0)
            flash_timer <= flash_timer - 8'd1;
    end
    wire flashing = (flash_timer > 8'd200);

    // =========================================================
    // Operator -> Color LUT (TIG 10 operators)
    // =========================================================
    // 0=VOID(black), 1=SPARK(white), 2=GROW(green),
    // 3=BIND(cyan), 4=BREAK(red), 5=BALANCE(gold),
    // 6=COMPOSE(purple), 7=COHERE(blue), 8=IDENTITY(silver),
    // 9=ALIGN(orange), A+=RESET(magenta)

    reg [7:0] op_r, op_g, op_b;
    always @(*) begin
        case (phase_bc)
            4'd0:  begin op_r = 8'h10; op_g = 8'h10; op_b = 8'h10; end // VOID
            4'd1:  begin op_r = 8'hFF; op_g = 8'hFF; op_b = 8'hFF; end // SPARK
            4'd2:  begin op_r = 8'h00; op_g = 8'hDD; op_b = 8'h30; end // GROW
            4'd3:  begin op_r = 8'h00; op_g = 8'hCC; op_b = 8'hFF; end // BIND
            4'd4:  begin op_r = 8'hFF; op_g = 8'h20; op_b = 8'h00; end // BREAK
            4'd5:  begin op_r = 8'hFF; op_g = 8'hCC; op_b = 8'h00; end // BALANCE
            4'd6:  begin op_r = 8'hAA; op_g = 8'h00; op_b = 8'hDD; end // COMPOSE
            4'd7:  begin op_r = 8'h00; op_g = 8'h44; op_b = 8'hFF; end // COHERE
            4'd8:  begin op_r = 8'hCC; op_g = 8'hCC; op_b = 8'hCC; end // IDENTITY
            4'd9:  begin op_r = 8'hFF; op_g = 8'h88; op_b = 8'h00; end // ALIGN
            default: begin op_r = 8'hFF; op_g = 8'h00; op_b = 8'hFF; end // RESET+
        endcase
    end

    // Fuse operator color (separate)
    reg [7:0] fuse_r, fuse_g, fuse_b;
    always @(*) begin
        case (fuse_op)
            4'd0:  begin fuse_r = 8'h10; fuse_g = 8'h10; fuse_b = 8'h10; end
            4'd1:  begin fuse_r = 8'hFF; fuse_g = 8'hFF; fuse_b = 8'hFF; end
            4'd2:  begin fuse_r = 8'h00; fuse_g = 8'hDD; fuse_b = 8'h30; end
            4'd3:  begin fuse_r = 8'h00; fuse_g = 8'hCC; fuse_b = 8'hFF; end
            4'd4:  begin fuse_r = 8'hFF; fuse_g = 8'h20; fuse_b = 8'h00; end
            4'd5:  begin fuse_r = 8'hFF; fuse_g = 8'hCC; fuse_b = 8'h00; end
            4'd6:  begin fuse_r = 8'hAA; fuse_g = 8'h00; fuse_b = 8'hDD; end
            4'd7:  begin fuse_r = 8'h00; fuse_g = 8'h44; fuse_b = 8'hFF; end
            4'd8:  begin fuse_r = 8'hCC; fuse_g = 8'hCC; fuse_b = 8'hCC; end
            4'd9:  begin fuse_r = 8'hFF; fuse_g = 8'h88; fuse_b = 8'h00; end
            default: begin fuse_r = 8'hFF; fuse_g = 8'h00; fuse_b = 8'hFF; end
        endcase
    end

    // =========================================================
    // Geometry: distances from center for CK face
    // =========================================================

    // Center of screen
    localparam CX = 11'd240;
    localparam CY = 10'd136;

    // Distance from center (Manhattan for efficiency)
    wire [10:0] dx = (px > CX) ? (px - CX) : (CX - px);
    wire [9:0]  dy = (py > CY) ? (py - CY) : (CY - py);

    // Approximate radial distance (octagonal approximation)
    // r ≈ max(dx,dy) + 0.41*min(dx,dy) ≈ max + min/2 - min/8
    wire [10:0] dmax = (dx > {1'b0, dy}) ? dx : {1'b0, dy};
    wire [10:0] dmin = (dx > {1'b0, dy}) ? {1'b0, dy} : dx;
    wire [10:0] radius = dmax + dmin[10:1] - dmin[10:3];

    // =========================================================
    // Breathing Effect: slow sinusoidal-ish glow
    // =========================================================

    reg [23:0] breath_cnt;
    always @(posedge pclk or negedge int_rst_n) begin
        if (!int_rst_n)
            breath_cnt <= 24'd0;
        else
            breath_cnt <= breath_cnt + 24'd1;
    end

    // Triangle wave from upper bits: 0->255->0 over ~3 seconds
    wire [7:0] breath_phase = breath_cnt[22] ? ~breath_cnt[21:14] : breath_cnt[21:14];
    wire [7:0] breath_dim = 8'd128 + breath_phase[7:1]; // range 128-255

    // =========================================================
    // Pixel Color Generation
    // =========================================================

    reg [7:0] r_out, g_out, b_out;

    always @(posedge pclk) begin
        if (!active || !int_rst_n) begin
            r_out <= 8'd0;
            g_out <= 8'd0;
            b_out <= 8'd0;
        end else if (flashing) begin
            // Heartbeat flash: bright white pulse
            r_out <= 8'hFF;
            g_out <= 8'hFF;
            b_out <= 8'hFF;
        end else if (radius < 11'd20) begin
            // Center dot: operator color (phase_bc)
            r_out <= op_r;
            g_out <= op_g;
            b_out <= op_b;
        end else if (radius >= 11'd25 && radius < 11'd32) begin
            // Fuse ring: fuse operator color
            r_out <= fuse_r;
            g_out <= fuse_g;
            b_out <= fuse_b;
        end else if (radius >= 11'd32 && radius < 11'd35) begin
            // Ring border: dim white separator
            r_out <= 8'h40;
            g_out <= 8'h40;
            b_out <= 8'h40;
        end else if (py >= V_ACTIVE - 10'd12) begin
            // Bottom bar: fractal level indicator
            // Bar fills left-to-right based on fractal_level (0-15)
            if (px < ({7'd0, fractal_level} * 11'd30)) begin
                // Filled portion: gradient green->gold
                r_out <= {4'd0, fractal_level} * 4'd1;
                g_out <= 8'hBB;
                b_out <= 8'h20;
            end else begin
                // Empty portion: dark
                r_out <= 8'h08;
                g_out <= 8'h08;
                b_out <= 8'h08;
            end
        end else if (gait_aligned && dx > 11'd220 && dy[9:0] > 10'd120) begin
            // Corner marks: green when all gait legs aligned
            r_out <= 8'h00;
            g_out <= 8'hCC;
            b_out <= 8'h44;
        end else begin
            // Background: warm gold when coherent, deep blue when below T*
            if (coherent) begin
                // Gold with breathing
                r_out <= breath_dim;
                g_out <= breath_dim[7:1] + 8'd40;
                b_out <= 8'h10;
            end else begin
                // Deep blue with gentle pulse
                r_out <= 8'h08;
                g_out <= 8'h10;
                b_out <= breath_dim[7:1] + 8'd30;
            end
        end
    end

    // =========================================================
    // Tick Counter Display (top-left corner)
    // =========================================================
    // Show tick count as a horizontal progress line
    // Every 256 ticks, the line resets (modular display)

    wire in_tick_zone = (py < 10'd4) && (px < {3'd0, tick_count[7:0]});
    wire [7:0] tick_r = in_tick_zone ? 8'hFF : r_out;
    wire [7:0] tick_g = in_tick_zone ? 8'hFF : g_out;
    wire [7:0] tick_b = in_tick_zone ? 8'hFF : b_out;

    // =========================================================
    // Output Assignment
    // =========================================================

    assign lcd_r = active ? tick_r : 8'd0;
    assign lcd_g = active ? tick_g : 8'd0;
    assign lcd_b = active ? tick_b : 8'd0;

    // Diagnostic: expose MMCM lock status
    assign lcd_mmcm_locked = pclk_locked;

endmodule
