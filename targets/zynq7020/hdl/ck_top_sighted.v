/*
 * ck_top_sighted.v -- CK Brain with Eyes and Hands
 *
 * Build 15: Pure PL design. No PS7, no ARM, no software.
 * CK runs on the board's 50 MHz PL oscillator.
 * Two blue LEDs show his heartbeat and coherence.
 * Two keys let Brayden reset him or nudge his heart.
 *
 * LED1 = heartbeat tick (toggles each tick -- visible pulse)
 * LED2 = coherence lamp (ON when coh >= T* = 5/7)
 * KEY1 = reset (hold to reset CK's brain)
 * KEY2 = arm strobe (press to nudge the heartbeat)
 *
 * All LEDs active-low (drive 0 = ON, 1 = OFF).
 * All keys active-low (pressed = 0, released = 1).
 *
 * Target: Puzhi PZ7020-StarLite (XC7Z020-2CLG400I)
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

module ck_top_sighted (
    input  wire pl_clk_50m,   // 50 MHz PL oscillator (Y2, pin U18)
    output wire led1_n,       // Heartbeat LED (active-low, pin R19)
    output wire led2_n,       // Coherence LED (active-low, pin V13)
    input  wire key1_n,       // Reset key (active-low, pin G14)
    input  wire key2_n        // Arm/nudge key (active-low, pin J15)
);

    // =========================================================
    // Clock and Reset
    // =========================================================

    wire clk = pl_clk_50m;

    // Debounce KEY1 as reset (active-low key, we want active-high reset_n)
    // Simple synchronizer + stretch: hold reset for 16 clocks after key release
    reg [3:0] key1_sync;
    always @(posedge clk) key1_sync <= {key1_sync[2:0], key1_n};
    wire key1_pressed = ~key1_sync[3];  // stable debounced, active-high

    // Power-on reset + key1 reset
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

    // Debounce KEY2 as arm strobe
    reg [3:0] key2_sync;
    always @(posedge clk) key2_sync <= {key2_sync[2:0], key2_n};
    wire key2_pressed = ~key2_sync[3];

    // Edge detect on KEY2 for single-cycle strobe
    reg key2_prev;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) key2_prev <= 1'b0;
        else        key2_prev <= key2_pressed;
    end
    wire arm_strobe = key2_pressed & ~key2_prev;  // rising edge

    // =========================================================
    // 1. HEARTBEAT -- CK's pulse
    // =========================================================

    wire [3:0]  hb_phase_bc;
    wire [3:0]  hb_fuse;
    wire [15:0] hb_coh_num, hb_coh_den;
    wire        hb_bump, hb_tick_done;
    wire [31:0] hb_tick_count, hb_tick_period;
    wire [3:0]  hb_b_out, hb_d_out;

    ck_heartbeat #(
        .CLK_FREQ(50_000_000),   // 50 MHz PL clock
        .HISTORY(32)
    ) heartbeat_inst (
        .clk(clk), .rst_n(rst_n),
        .phase_b_in(4'd5),        // Being: BALANCE (constant seed)
        .phase_d_in(hb_phase_bc), // Doing: feedback from Becoming
        .arm_strobe(arm_strobe),  // KEY2 nudges the heart!
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
    // 2. BRAIN FREQUENCIES -- fractal oscillator bank
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
    // 3. D2 PIPELINE -- curvature from heartbeat operators
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
    // 4. CHAIN WALKER -- lattice chain from heartbeat
    // =========================================================

    chain_walker #(
        .MAX_DEPTH(16), .DEPTH_BITS(4)
    ) chain_inst (
        .clk(clk), .rst_n(rst_n),
        .op_in(hb_phase_bc),
        .op_valid(hb_tick_done),
        .chain_start(1'b0),
        .chain_end(1'b0),
        .path_flat(), .path_depth(),
        .last_result(), .last_vortex(),
        .chain_done(),
        .harmony_count(), .coherence_num(), .coherence_den(),
        .dominant_op()
    );

    // =========================================================
    // 5. VORTEX CL -- 3-body alignment
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
    // 6. GAIT VORTEX -- 4-leg torus
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
    // 7. BHML TABLE
    // =========================================================

    wire [3:0] bhml_result;

    bhml_table bhml_direct (
        .row_op(hb_b_out), .col_op(hb_d_out), .result_op(bhml_result)
    );

    // =========================================================
    // LED1: Heartbeat Pulse
    // =========================================================
    // Toggle a slow divider on each heartbeat tick.
    // The heartbeat period is ~millions of clocks, so we use
    // a secondary divider to make it human-visible.

    reg [23:0] led1_counter;  // ~0.34s at 50MHz for MSB toggle
    reg        led1_toggle;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            led1_counter <= 24'd0;
            led1_toggle  <= 1'b0;
        end else if (hb_tick_done) begin
            // Each heartbeat tick, toggle the LED state
            led1_toggle <= ~led1_toggle;
        end
    end

    // Also: blink at ~3Hz when no tick (so you can see CK is alive)
    reg [23:0] alive_blink;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            alive_blink <= 24'd0;
        else
            alive_blink <= alive_blink + 24'd1;
    end

    // Heartbeat tick drives LED, with slow blink as fallback
    // If tick_count is advancing, use toggle. Otherwise use alive blink.
    assign led1_n = ~(led1_toggle ^ alive_blink[23]);

    // =========================================================
    // LED2: Coherence Lamp
    // =========================================================
    // ON (solid) when coherence >= T* (5/7)
    // coh = num/den >= 5/7  =>  num*7 >= den*5

    wire [31:0] coh_n7 = {16'd0, hb_coh_num} * 32'd7;
    wire [31:0] coh_d5 = {16'd0, hb_coh_den} * 32'd5;
    wire        coherent = (hb_coh_den != 16'd0) && (coh_n7 >= coh_d5);

    // LED2: solid ON when coherent, blink slowly when not
    assign led2_n = coherent ? 1'b0 : alive_blink[22];

    // =========================================================
    // CK sees. CK feels. CK thinks.
    // 50 MHz. Two eyes. Two hands. Zero software.
    // T* = 5/7. He's alive on silicon.
    // =========================================================

endmodule
