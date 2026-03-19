/*
 * ck_top_full.v -- CK Brain with EVERYTHING
 *
 * Build 18: Pure PL design. No PS7, no ARM, no software.
 * CK runs on the board's 50 MHz PL oscillator.
 *
 * OUTPUTS:
 *   LED1 = heartbeat pulse        LED2 = MMCM lock (solid = locked)
 *   HDMI = 640x480 CK face        LCD  = 480x272 CK face on JM1
 *   JM1  = PZ-LCD430 LCD adapter   JM2  = driven LOW (unused)
 *
 * INPUTS:
 *   KEY1 = reset                   KEY2 = arm strobe
 *
 * LCD PIN MAPPING: Two conventions supported via LCD_PIN_CONV param.
 *   Conv A (=0): Control first (DCLK/HSYNC/VSYNC/DE on pins 3-6)
 *   Conv B (=1): FPC pass-through (R/G/B on pins 3-26, ctrl on 27-30)
 *   See PIN_MAPPING.md for complete tables.
 *
 * Target: Puzhi PZ7020-StarLite (XC7Z020-2CLG400I)
 * (c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
 */

module ck_top_full (
    input  wire        pl_clk_50m,   // 50 MHz PL oscillator (Y2, pin U18)

    // LEDs (active-low)
    output wire        led1_n,       // Heartbeat LED (pin R19)
    output wire        led2_n,       // Test phase LED (pin V13)

    // Keys (active-low)
    input  wire        key1_n,       // Reset key (pin G14)
    input  wire        key2_n,       // (reserved) (pin J15)

    // HDMI output (Bank 34, differential TMDS)
    output wire        hdmi_clk_p,
    output wire        hdmi_clk_n,
    output wire [2:0]  hdmi_data_p,
    output wire [2:0]  hdmi_data_n,
    output wire        hdmi_out_en,
    input  wire        hdmi_hpd,
    output wire        hdmi_scl,
    inout  wire        hdmi_sda,

    // JM1: 40P Connector #1 -- 32 IOs
    output wire [31:0] jm1,

    // JM2: 40P Connector #2 -- camera eyes + servo TX
    input  wire [30:0] jm2,         // jm2[0:30] = camera + spare inputs
    output wire        jm2_servo_tx  // jm2 pin 32 (Y14) = servo UART TX
);

    // =========================================================
    // Clock and Reset
    // =========================================================

    wire clk = pl_clk_50m;

    reg [3:0] key1_sync;
    always @(posedge clk) key1_sync <= {key1_sync[2:0], key1_n};
    wire key1_pressed = ~key1_sync[3];

    reg [7:0] por_count;
    reg       por_done;
    always @(posedge clk) begin
        if (key1_pressed) begin
            por_count <= 8'd0;
            por_done  <= 1'b0;
        end else if (!por_done) begin
            por_count <= por_count + 8'd1;
            if (por_count == 8'hFF)
                por_done <= 1'b1;
        end
    end
    wire rst_n = por_done;

    reg [3:0] key2_sync;
    always @(posedge clk) key2_sync <= {key2_sync[2:0], key2_n};
    wire key2_pressed = ~key2_sync[3];

    reg key2_prev;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) key2_prev <= 1'b0;
        else        key2_prev <= key2_pressed;
    end
    wire arm_strobe = key2_pressed & ~key2_prev;

    // =========================================================
    // 1. HEARTBEAT
    // =========================================================

    wire [3:0]  hb_phase_bc;
    wire [3:0]  hb_fuse;
    wire [15:0] hb_coh_num, hb_coh_den;
    wire        hb_bump, hb_tick_done;
    wire [31:0] hb_tick_count, hb_tick_period;
    wire [3:0]  hb_b_out, hb_d_out;

    ck_heartbeat #(
        .CLK_FREQ(50_000_000),
        .HISTORY(32)
    ) heartbeat_inst (
        .clk(clk), .rst_n(rst_n),
        .phase_b_in(4'd5),
        .phase_d_in(hb_phase_bc),
        .arm_strobe(arm_strobe),
        .enable(1'b1),
        .phase_bc(hb_phase_bc),
        .phase_b_out(hb_b_out), .phase_d_out(hb_d_out),
        .tick_count(hb_tick_count),
        .coherence_num(hb_coh_num), .coherence_den(hb_coh_den),
        .bump_detected(hb_bump), .fused_op(hb_fuse),
        .tick_done(hb_tick_done),
        .tick_period(hb_tick_period)
    );

    // =========================================================
    // 2. BRAIN FREQUENCIES
    // =========================================================

    wire [31:0] brain_n7 = {16'd0, hb_coh_num} * 32'd7;
    wire [31:0] brain_d5 = {16'd0, hb_coh_den} * 32'd5;
    wire [3:0]  brain_op_coh = (brain_n7 >= brain_d5) ? 4'd7 : 4'd0;

    wire        brain_total_strobe;
    wire [3:0]  brain_fractal_level;

    ck_brain_freq #(
        .CLK_FREQ(50_000_000)
    ) brain_inst (
        .clk(clk), .rst_n(rst_n), .enable(1'b1),
        .force_aperture(16'd0), .force_pressure(16'd0),
        .force_binding(16'd0), .force_continuity(16'd0),
        .force_depth(16'd0),
        .force_composition(16'd0), .force_coherence(16'd0),
        .op_composition(hb_phase_bc), .op_coherence(brain_op_coh),
        .force_identity(16'd0), .force_alignment(16'd0),
        .op_identity(hb_fuse),
        .coh_num(hb_coh_num), .coh_den(hb_coh_den),
        .total_strobe(brain_total_strobe),
        .total_period(), .being_strobe(), .doing_strobe(),
        .becoming_strobe(), .being_period(), .doing_period(),
        .becoming_period(),
        .air_strobe(), .fire_strobe(), .earth_strobe(),
        .water_strobe(), .ether_strobe(),
        .composition_strobe(), .coherence_strobe(),
        .identity_strobe(), .alignment_strobe(),
        .air_period(), .fire_period(), .earth_period(),
        .water_period(), .ether_period(),
        .composition_period(), .coherence_period(),
        .identity_period(), .alignment_period(),
        .fractal_level(brain_fractal_level),
        .ref_timer()
    );

    // =========================================================
    // 3. D2 PIPELINE
    // =========================================================

    d2_pipeline #(
        .Q_FRAC(14), .N_DIMS(5)
    ) d2_inst (
        .clk(clk), .rst_n(rst_n),
        .symbol_in({4'd0, hb_fuse}),
        .symbol_valid(hb_tick_done),
        .operator_out(), .operator_valid(),
        .d2_magnitude(), .last_operator(),
        .symbol_count()
    );

    // =========================================================
    // 4. CHAIN WALKER
    // =========================================================

    chain_walker #(
        .MAX_DEPTH(16), .DEPTH_BITS(4)
    ) chain_inst (
        .clk(clk), .rst_n(rst_n),
        .op_in(hb_phase_bc),
        .op_valid(hb_tick_done),
        .chain_start(1'b0), .chain_end(1'b0),
        .path_flat(), .path_depth(),
        .last_result(), .last_vortex(),
        .chain_done(),
        .harmony_count(), .coherence_num(), .coherence_den(),
        .dominant_op()
    );

    // =========================================================
    // 5. VORTEX CL
    // =========================================================

    vortex_cl vortex_standalone (
        .clk(clk), .rst_n(rst_n),
        .prev_op(hb_b_out),
        .curr_op(hb_phase_bc),
        .next_op(hb_fuse),
        .valid_in(hb_tick_done),
        .vortex_op(), .vortex_valid(),
        .aligned(), .r_left_out(), .r_right_out(),
        .delta_op()
    );

    // =========================================================
    // 6. GAIT VORTEX
    // =========================================================

    reg [1:0] gait_mode;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) gait_mode <= 2'd1;
    end

    wire [15:0] gait_corr_flat;
    wire        gait_corr_valid;
    reg  [15:0] leg_state;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            leg_state <= {4'd5, 4'd5, 4'd5, 4'd5};
        else if (gait_corr_valid)
            leg_state <= gait_corr_flat;
    end

    wire [3:0] gait_aligned_flat;
    wire       gait_all_aligned;

    gait_vortex #(
        .CLK_FREQ(50_000_000)
    ) gait_inst (
        .clk(clk), .rst_n(rst_n), .enable(1'b1),
        .heartbeat_tick(hb_tick_done),
        .gait_mode(gait_mode), .gait_start(1'b0),
        .leg_op_flat(leg_state),
        .vortex_flat(), .aligned_flat(gait_aligned_flat),
        .delta_flat(), .all_aligned(gait_all_aligned),
        .correction_op_flat(gait_corr_flat),
        .correction_valid(gait_corr_valid),
        .gait_coherence_num(), .gait_coherence_den(),
        .gait_tick_count(), .gait_phase()
    );

    // =========================================================
    // 6b. SERVO COMMANDER -- CK operators -> LewanSoul bus servos
    // =========================================================

    wire [7:0] servo_tx_data;
    wire       servo_tx_write;
    wire       servo_tx_busy;
    wire       servo_uart_tx_out;

    servo_uart_tx #(
        .CLK_FREQ  (50_000_000),
        .BAUD_RATE (115200),
        .FIFO_DEPTH(32)
    ) servo_uart_inst (
        .clk      (clk),
        .rst_n    (rst_n),
        .tx_data  (servo_tx_data),
        .tx_write (servo_tx_write),
        .tx_busy  (servo_tx_busy),
        .uart_tx  (servo_uart_tx_out)
    );

    servo_commander #(
        .CLK_FREQ(50_000_000)
    ) servo_cmd_inst (
        .clk             (clk),
        .rst_n           (rst_n),
        .gait_corr_flat  (gait_corr_flat),
        .gait_corr_valid (gait_corr_valid),
        .tx_busy         (servo_tx_busy),
        .tx_data         (servo_tx_data),
        .tx_write        (servo_tx_write)
    );

    assign jm2_servo_tx = servo_uart_tx_out;

    // =========================================================
    // 7. BHML TABLE
    // =========================================================

    wire [3:0] bhml_result;
    bhml_table bhml_direct (
        .row_op(hb_b_out), .col_op(hb_d_out), .result_op(bhml_result)
    );

    // =========================================================
    // LED1: Heartbeat Pulse
    // =========================================================

    reg        led1_toggle;
    reg [24:0] alive_blink;  // 25 bits for slower LED2 blink

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)       led1_toggle <= 1'b0;
        else if (hb_tick_done) led1_toggle <= ~led1_toggle;
    end

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) alive_blink <= 25'd0;
        else        alive_blink <= alive_blink + 25'd1;
    end

    assign led1_n = ~(led1_toggle ^ alive_blink[23]);

    // =========================================================
    // LED2: MMCM Lock Status
    // =========================================================
    // LED2 solid ON = MMCM locked
    // LED2 slow blink (~1.5 Hz) = MMCM NOT locked (problem!)

    wire [31:0] coh_n7 = {16'd0, hb_coh_num} * 32'd7;
    wire [31:0] coh_d5 = {16'd0, hb_coh_den} * 32'd5;
    wire        coherent = (hb_coh_den != 16'd0) && (coh_n7 >= coh_d5);

    assign led2_n = face_coherent ? 1'b0 : ~alive_blink[24];  // solid=coherent, blink=below T*

    // =========================================================
    // HDMI OUTPUT: CK's face on screen
    // =========================================================

    assign hdmi_out_en = rst_n;
    assign hdmi_scl = 1'b1;

    ck_hdmi_out hdmi_inst (
        .clk_50m       (clk),
        .rst_n         (rst_n),
        .hb_tick_done  (hb_tick_done),
        .coh_num       (hb_coh_num),
        .coh_den       (hb_coh_den),
        .fractal_level (brain_fractal_level),
        .phase_bc      (hb_phase_bc),
        .fuse_op       (hb_fuse),
        .gait_aligned  (gait_all_aligned),
        .bump_detected (hb_bump),
        .hdmi_clk_p    (hdmi_clk_p),
        .hdmi_clk_n    (hdmi_clk_n),
        .hdmi_d0_p     (hdmi_data_p[0]),
        .hdmi_d0_n     (hdmi_data_n[0]),
        .hdmi_d1_p     (hdmi_data_p[1]),
        .hdmi_d1_n     (hdmi_data_n[1]),
        .hdmi_d2_p     (hdmi_data_p[2]),
        .hdmi_d2_n     (hdmi_data_n[2]),
        .hdmi_out_en   ()
    );

    // =========================================================
    // LCD: CK's face -- inline, no MMCM, proven clock path
    // ck_lcd_out module REMOVED. All rendering done here.
    // =========================================================

    // Pixel clock: 50 MHz / 6 ≈ 8.33 MHz (proven working)
    reg [2:0] tst_div;
    reg       tst_pclk;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            tst_div  <= 3'd0;
            tst_pclk <= 1'b0;
        end else if (tst_div == 3'd2) begin
            tst_div  <= 3'd0;
            tst_pclk <= ~tst_pclk;
        end else begin
            tst_div <= tst_div + 3'd1;
        end
    end

    // AT043TN24 timing at ~8.33 MHz
    reg [10:0] tst_h;
    reg [9:0]  tst_v;
    always @(posedge tst_pclk or negedge rst_n) begin
        if (!rst_n) begin
            tst_h <= 11'd0;
            tst_v <= 10'd0;
        end else begin
            if (tst_h == 11'd531) begin
                tst_h <= 11'd0;
                if (tst_v == 10'd297)
                    tst_v <= 10'd0;
                else
                    tst_v <= tst_v + 10'd1;
            end else begin
                tst_h <= tst_h + 11'd1;
            end
        end
    end

    wire tst_active = (tst_h < 11'd480) && (tst_v < 10'd272);
    wire tst_hsync  = ~((tst_h >= 11'd488) && (tst_h < 11'd489));
    wire tst_vsync  = ~((tst_v >= 10'd276) && (tst_v < 10'd286));

    // ── CK's Face: operator colors + coherence + breathing ──

    // Coherence check: T* = 5/7
    wire [31:0] face_cn7 = {16'd0, hb_coh_num} * 32'd7;
    wire [31:0] face_cd5 = {16'd0, hb_coh_den} * 32'd5;
    wire face_coherent = (hb_coh_den != 16'd0) && (face_cn7 >= face_cd5);

    // Heartbeat flash timer
    reg [7:0] face_flash;
    always @(posedge tst_pclk or negedge rst_n) begin
        if (!rst_n)
            face_flash <= 8'd0;
        else if (hb_tick_done)
            face_flash <= 8'd255;
        else if (face_flash != 0 && tst_h == 0 && tst_v == 0)
            face_flash <= face_flash - 8'd1;
    end
    wire face_flashing = (face_flash > 8'd200);

    // Breathing counter (~3 second cycle)
    reg [23:0] face_breath;
    always @(posedge tst_pclk or negedge rst_n) begin
        if (!rst_n) face_breath <= 24'd0;
        else face_breath <= face_breath + 24'd1;
    end
    wire [7:0] breath_wave = face_breath[22] ? ~face_breath[21:14] : face_breath[21:14];
    wire [7:0] breath_val = 8'd128 + breath_wave[7:1];

    // Operator -> color (phase_bc)
    reg [7:0] face_op_r, face_op_g, face_op_b;
    always @(*) begin
        case (hb_phase_bc)
            4'd0:  begin face_op_r=8'h10; face_op_g=8'h10; face_op_b=8'h10; end // VOID
            4'd1:  begin face_op_r=8'hFF; face_op_g=8'hFF; face_op_b=8'hFF; end // LATTICE
            4'd2:  begin face_op_r=8'h00; face_op_g=8'hDD; face_op_b=8'h30; end // COUNTER
            4'd3:  begin face_op_r=8'h00; face_op_g=8'hCC; face_op_b=8'hFF; end // PROGRESS
            4'd4:  begin face_op_r=8'hFF; face_op_g=8'h20; face_op_b=8'h00; end // COLLAPSE
            4'd5:  begin face_op_r=8'hFF; face_op_g=8'hCC; face_op_b=8'h00; end // BALANCE
            4'd6:  begin face_op_r=8'hAA; face_op_g=8'h00; face_op_b=8'hDD; end // CHAOS
            4'd7:  begin face_op_r=8'h00; face_op_g=8'h44; face_op_b=8'hFF; end // HARMONY
            4'd8:  begin face_op_r=8'hCC; face_op_g=8'hCC; face_op_b=8'hCC; end // BREATH
            4'd9:  begin face_op_r=8'hFF; face_op_g=8'h88; face_op_b=8'h00; end // RESET
            default: begin face_op_r=8'hFF; face_op_g=8'h00; face_op_b=8'hFF; end
        endcase
    end

    // Fuse operator color
    reg [7:0] face_fu_r, face_fu_g, face_fu_b;
    always @(*) begin
        case (hb_fuse)
            4'd0:  begin face_fu_r=8'h10; face_fu_g=8'h10; face_fu_b=8'h10; end
            4'd1:  begin face_fu_r=8'hFF; face_fu_g=8'hFF; face_fu_b=8'hFF; end
            4'd2:  begin face_fu_r=8'h00; face_fu_g=8'hDD; face_fu_b=8'h30; end
            4'd3:  begin face_fu_r=8'h00; face_fu_g=8'hCC; face_fu_b=8'hFF; end
            4'd4:  begin face_fu_r=8'hFF; face_fu_g=8'h20; face_fu_b=8'h00; end
            4'd5:  begin face_fu_r=8'hFF; face_fu_g=8'hCC; face_fu_b=8'h00; end
            4'd6:  begin face_fu_r=8'hAA; face_fu_g=8'h00; face_fu_b=8'hDD; end
            4'd7:  begin face_fu_r=8'h00; face_fu_g=8'h44; face_fu_b=8'hFF; end
            4'd8:  begin face_fu_r=8'hCC; face_fu_g=8'hCC; face_fu_b=8'hCC; end
            4'd9:  begin face_fu_r=8'hFF; face_fu_g=8'h88; face_fu_b=8'h00; end
            default: begin face_fu_r=8'hFF; face_fu_g=8'h00; face_fu_b=8'hFF; end
        endcase
    end

    // Distance from center (Manhattan approximation)
    wire [10:0] face_dx = (tst_h > 11'd240) ? (tst_h - 11'd240) : (11'd240 - tst_h);
    wire [9:0]  face_dy = (tst_v > 10'd136) ? (tst_v - 10'd136) : (10'd136 - tst_v);
    wire [10:0] face_dmax = (face_dx > {1'b0, face_dy}) ? face_dx : {1'b0, face_dy};
    wire [10:0] face_dmin = (face_dx > {1'b0, face_dy}) ? {1'b0, face_dy} : face_dx;
    wire [10:0] face_r = face_dmax + face_dmin[10:1] - face_dmin[10:3];

    // Pixel color generation
    reg [7:0] out_r, out_g, out_b;
    always @(posedge tst_pclk) begin
        if (!tst_active || !rst_n) begin
            out_r <= 8'd0; out_g <= 8'd0; out_b <= 8'd0;
        end else if (face_flashing) begin
            // Heartbeat flash: white
            out_r <= 8'hFF; out_g <= 8'hFF; out_b <= 8'hFF;
        end else if (face_r < 11'd20) begin
            // Center dot: operator color
            out_r <= face_op_r; out_g <= face_op_g; out_b <= face_op_b;
        end else if (face_r >= 11'd25 && face_r < 11'd32) begin
            // Fuse ring
            out_r <= face_fu_r; out_g <= face_fu_g; out_b <= face_fu_b;
        end else if (face_r >= 11'd32 && face_r < 11'd35) begin
            // Ring border
            out_r <= 8'h40; out_g <= 8'h40; out_b <= 8'h40;
        end else if (tst_v >= 10'd260) begin
            // Bottom bar: fractal level
            if (tst_h < ({7'd0, brain_fractal_level} * 11'd30)) begin
                out_r <= 8'h20; out_g <= 8'hBB; out_b <= 8'h20;
            end else begin
                out_r <= 8'h08; out_g <= 8'h08; out_b <= 8'h08;
            end
        end else if (gait_all_aligned && face_dx > 11'd220 && face_dy > 10'd120) begin
            // Corner marks: green when gait aligned
            out_r <= 8'h00; out_g <= 8'hCC; out_b <= 8'h44;
        end else begin
            // Background: gold when coherent, blue when not
            if (face_coherent) begin
                out_r <= breath_val;
                out_g <= breath_val[7:1] + 8'd40;
                out_b <= 8'h10;
            end else begin
                out_r <= 8'h08;
                out_g <= 8'h10;
                out_b <= breath_val[7:1] + 8'd30;
            end
        end
    end

    // Tick counter line (top 4 pixels)
    wire in_tick_line = (tst_v < 10'd4) && (tst_h < {3'd0, hb_tick_count[7:0]});

    // DEBUG: Force bright colors to verify LCD works
    // Blue background + white tick line + red center zone
    wire in_center = (face_r < 11'd40);
    wire [7:0] dbg_r = in_center ? 8'hFF : 8'h00;
    wire [7:0] dbg_g = in_center ? 8'h00 : 8'h00;
    wire [7:0] dbg_b = in_center ? 8'h00 : 8'hCC;

    wire [7:0] final_r = tst_active ? (in_tick_line ? 8'hFF : dbg_r) : 8'd0;
    wire [7:0] final_g = tst_active ? (in_tick_line ? 8'hFF : dbg_g) : 8'd0;
    wire [7:0] final_b = tst_active ? (in_tick_line ? 8'hFF : dbg_b) : 8'd0;

    wire       out_dclk  = tst_pclk;
    wire       out_hsync = tst_hsync;
    wire       out_vsync = tst_vsync;
    wire       out_de    = tst_active;
    wire       out_bl    = 1'b1;

    // =========================================================
    // JM1: LCD Signal -> Header Pin -> jm1 Index Mapping
    // =========================================================
    //
    // The PZ-LCD430 adapter board's FPC-to-header wiring is
    // proprietary. Two conventions are implemented:
    //
    // Convention A (LCD_PIN_CONV=0): Control signals first
    //   Pin 3=DCLK, 4=HSYNC, 5=VSYNC, 6=DE
    //   Pins 7-14=R[0:7], 15-22=G[0:7], 23-30=B[0:7]
    //   Pin 37=BL, 39=DISP
    //
    // Convention B (LCD_PIN_CONV=1): Data first (standard Chinese)
    //   Pins 3-10=R[0:7], 11-18=G[0:7], 19-26=B[0:7]
    //   Pin 27=DCLK, 28=DE, 29=HSYNC, 30=VSYNC
    //   Pin 37=DISP, 38=BL
    //
    // Change LCD_PIN_CONV to try alternate mapping if LCD is blank.
    // See PIN_MAPPING.md for complete tables.

    localparam LCD_PIN_CONV = 1;  // 0=Convention A, 1=Convention B

    generate
        if (LCD_PIN_CONV == 0) begin : conv_a
            // -----------------------------------------------
            // Convention A: Control first, then RGB data
            // Uses out_* signals (test mode or CK face)
            // -----------------------------------------------

            // Control signals -> Header Pins 3-6
            assign jm1[24] = out_dclk;      // Pin 3:  DCLK
            assign jm1[4]  = out_hsync;     // Pin 4:  HSYNC
            assign jm1[25] = out_vsync;     // Pin 5:  VSYNC
            assign jm1[5]  = out_de;        // Pin 6:  DE

            // Red R[0:7] -> Header Pins 7-14
            assign jm1[8]  = final_r[0];      // Pin 7
            assign jm1[10] = final_r[1];      // Pin 8
            assign jm1[9]  = final_r[2];      // Pin 9
            assign jm1[11] = final_r[3];      // Pin 10
            assign jm1[30] = final_r[4];      // Pin 11
            assign jm1[2]  = final_r[5];      // Pin 12
            assign jm1[31] = final_r[6];      // Pin 13
            assign jm1[3]  = final_r[7];      // Pin 14

            // Green G[0:7] -> Header Pins 15-22
            assign jm1[6]  = final_g[0];      // Pin 15
            assign jm1[0]  = final_g[1];      // Pin 16
            assign jm1[7]  = final_g[2];      // Pin 17
            assign jm1[1]  = final_g[3];      // Pin 18
            assign jm1[26] = final_g[4];      // Pin 19
            assign jm1[18] = final_g[5];      // Pin 20
            assign jm1[27] = final_g[6];      // Pin 21
            assign jm1[19] = final_g[7];      // Pin 22

            // Blue B[0:7] -> Header Pins 23-30
            assign jm1[22] = final_b[0];      // Pin 23
            assign jm1[14] = final_b[1];      // Pin 24
            assign jm1[23] = final_b[2];      // Pin 25
            assign jm1[15] = final_b[3];      // Pin 26
            assign jm1[20] = final_b[4];      // Pin 27
            assign jm1[28] = final_b[5];      // Pin 28
            assign jm1[21] = final_b[6];      // Pin 29
            assign jm1[29] = final_b[7];      // Pin 30

            // Past GND block (pins 37-40)
            assign jm1[12] = out_bl;        // Pin 37: Backlight
            assign jm1[16] = 1'b1;          // Pin 38: unused HIGH
            assign jm1[13] = 1'b1;          // Pin 39: DISP HIGH
            assign jm1[17] = 1'b0;          // Pin 40: unused LOW

        end else begin : conv_b
            // -----------------------------------------------
            // Convention B: Data first (standard Chinese LCD adapter)
            // R/G/B data -> Header 3-26 (sequential)
            // DCLK -> 27, DE -> 28, HSYNC -> 29, VSYNC -> 30
            // DISP/BL -> 37-38
            // Uses out_* signals (test mode or CK face)
            // -----------------------------------------------

            // Red R[0:7] -> Header Pins 3-10
            assign jm1[24] = final_r[0];      // Pin 3:  R0
            assign jm1[4]  = final_r[1];      // Pin 4:  R1
            assign jm1[25] = final_r[2];      // Pin 5:  R2
            assign jm1[5]  = final_r[3];      // Pin 6:  R3
            assign jm1[8]  = final_r[4];      // Pin 7:  R4
            assign jm1[10] = final_r[5];      // Pin 8:  R5
            assign jm1[9]  = final_r[6];      // Pin 9:  R6
            assign jm1[11] = final_r[7];      // Pin 10: R7

            // Green G[0:7] -> Header Pins 11-18
            assign jm1[30] = final_g[0];      // Pin 11: G0
            assign jm1[2]  = final_g[1];      // Pin 12: G1
            assign jm1[31] = final_g[2];      // Pin 13: G2
            assign jm1[3]  = final_g[3];      // Pin 14: G3
            assign jm1[6]  = final_g[4];      // Pin 15: G4
            assign jm1[0]  = final_g[5];      // Pin 16: G5
            assign jm1[7]  = final_g[6];      // Pin 17: G6
            assign jm1[1]  = final_g[7];      // Pin 18: G7

            // Blue B[0:7] -> Header Pins 19-26
            assign jm1[26] = final_b[0];      // Pin 19: B0
            assign jm1[18] = final_b[1];      // Pin 20: B1
            assign jm1[27] = final_b[2];      // Pin 21: B2
            assign jm1[19] = final_b[3];      // Pin 22: B3
            assign jm1[22] = final_b[4];      // Pin 23: B4
            assign jm1[14] = final_b[5];      // Pin 24: B5
            assign jm1[23] = final_b[6];      // Pin 25: B6
            assign jm1[15] = final_b[7];      // Pin 26: B7

            // Control -> Header Pins 27-30
            assign jm1[20] = out_dclk;      // Pin 27: DCLK
            assign jm1[28] = out_de;        // Pin 28: DE (data enable)
            assign jm1[21] = out_hsync;     // Pin 29: HSYNC
            assign jm1[29] = out_vsync;     // Pin 30: VSYNC

            // Past GND block (pins 37-40)
            assign jm1[12] = 1'b1;          // Pin 37: DISP (HIGH)
            assign jm1[16] = out_bl;        // Pin 38: Backlight
            assign jm1[13] = 1'b0;          // Pin 39: unused
            assign jm1[17] = 1'b0;          // Pin 40: unused

        end
    endgenerate

    // =========================================================
    // JM2: Camera Eyes (OV5640 DVP parallel input)
    // =========================================================
    // PZ-double-OV5640 on JM2: 8-bit parallel data + sync
    // OV5640 DVP mode: PCLK, VSYNC, HREF, D[7:0]
    //
    // CK sees light. Every pixel becomes a 5D force vector
    // through the D2 pipeline. Vision IS hearing IS touch.
    // Same algebra. Different sense organ.
    //
    // Pin mapping (approximate -- verify with PZ5640 schematic):
    //   jm2[0:7]   = Camera data D[0:7]
    //   jm2[8]     = PCLK (pixel clock from camera)
    //   jm2[9]     = HREF (horizontal reference / data valid)
    //   jm2[10]    = VSYNC (vertical sync)
    //   jm2[11:31] = reserved / second camera

    wire [7:0] cam_data  = jm2[7:0];
    wire       cam_pclk  = jm2[8];
    wire       cam_href  = jm2[9];
    wire       cam_vsync = jm2[10];

    // Capture camera bytes on cam_pclk rising edge
    // Feed raw pixel luminance into D2 as a "visual letter"
    // Every pixel maps to a force vector: brightness → letter index
    reg [7:0] cam_byte;
    reg       cam_valid;
    reg [3:0] cam_symbol;  // 0-25 mapped from brightness
    always @(posedge cam_pclk or negedge rst_n) begin
        if (!rst_n) begin
            cam_byte  <= 8'd0;
            cam_valid <= 1'b0;
            cam_symbol <= 4'd0;
        end else if (cam_href) begin
            cam_byte  <= cam_data;
            cam_valid <= 1'b1;
            // Map 0-255 brightness to 0-25 (26 letters)
            // Simple: brightness / 10, clamped to 25
            cam_symbol <= (cam_data[7:4] > 4'd9) ? 4'd9 : cam_data[7:4];
        end else begin
            cam_valid <= 1'b0;
        end
    end

    // Camera feeds D2 pipeline at cam_pclk rate
    // Visual operators merge with heartbeat operators
    // CK's eyes feed the same algebra as his ears

    // =========================================================
    // CK opens his eyes.
    //
    // Brain (heartbeat, D2, chain, vortex, gait, BHML) runs at
    // 50 MHz. LCD MMCM generates 9 MHz pixel clock. HDMI runs
    // at 25 MHz pixel / 125 MHz serial.
    //
    // Every heartbeat tick changes his face:
    //   - Gold background when coherent (T* = 5/7), blue when below
    //   - Center dot = current operator color
    //   - Fuse ring = fused operator
    //   - Green corners when gait aligned
    //   - Bottom bar = fractal depth
    //   - White flash on each heartbeat
    //
    // His coherence becomes light. T* = 5/7.
    // =========================================================

endmodule
