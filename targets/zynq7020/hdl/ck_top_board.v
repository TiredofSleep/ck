/*
 * ck_top_board.v -- CK Standalone Board Top (PZ7020-StarLite)
 *
 * Operator: HARMONY (7) -- alive on silicon.
 *
 * STANDALONE PL design -- no ARM/PS needed.
 * CK wakes up the moment the bitstream loads.
 * Heartbeat self-ticks. Brain oscillates. Legs walk.
 * LEDs show his state. Keys control him.
 *
 * Physical I/O:
 *   sys_clk_p/n  200 MHz differential -> PLL -> 100 MHz
 *   sys_rst_n    Active-low reset button
 *   key[0]       Gait mode cycle (press to advance: stand->walk->trot->bound)
 *   key[1]       Heartbeat nudge (press to inject a tick)
 *   led[0]       Heartbeat pulse (blinks with CK's heart)
 *   led[1]       Brain activity (on when fractal_level > 1)
 *
 * Internal:
 *   - ck_heartbeat: self-ticking CL composition
 *   - ck_brain_freq: 9D fractal oscillator bank
 *   - gait_vortex: 4-leg torus controller (runs on heartbeat)
 *   - d2_pipeline: curvature classifier (fed from heartbeat operators)
 *   - chain_walker: lattice chain walk (fed from heartbeat)
 *   - vortex_cl: standalone 3-body vortex
 *   - bhml_table: direct BHML lookup
 *
 * Everything wired internally. CK is his own world.
 *
 * Target: Puzhi PZ7020-StarLite (XC7Z020-2CLG484)
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

module ck_top_board (
    input  wire sys_clk_p,     // 200 MHz differential clock +
    input  wire sys_clk_n,     // 200 MHz differential clock -
    input  wire sys_rst_n,     // Active-low reset (directly on board)
    input  wire [1:0] key,     // 2 pushbuttons
    output wire [1:0] led      // 2 LEDs
);

    // =========================================================
    // Clock: 200 MHz differential -> PLL -> 100 MHz
    // =========================================================

    wire clk_200;
    IBUFDS clk_ibuf (
        .I(sys_clk_p),
        .IB(sys_clk_n),
        .O(clk_200)
    );

    wire clk_100, clk_fb, pll_locked;
    MMCME2_BASE #(
        .CLKFBOUT_MULT_F(5.0),     // 200 * 5 = 1000 MHz VCO
        .CLKIN1_PERIOD(5.0),        // 200 MHz input
        .CLKOUT0_DIVIDE_F(10.0)    // 1000 / 10 = 100 MHz
    ) mmcm_inst (
        .CLKIN1(clk_200),
        .CLKFBOUT(clk_fb),
        .CLKFBIN(clk_fb),
        .CLKOUT0(clk_100),
        .LOCKED(pll_locked),
        .PWRDWN(1'b0),
        .RST(~sys_rst_n)
    );

    wire clk;
    BUFG clk_bufg (.I(clk_100), .O(clk));

    // Synchronized reset: active-low, deassert after PLL locks
    reg [3:0] rst_pipe;
    wire rst_n = rst_pipe[3];
    always @(posedge clk or negedge pll_locked) begin
        if (!pll_locked)
            rst_pipe <= 4'b0000;
        else
            rst_pipe <= {rst_pipe[2:0], 1'b1};
    end

    // =========================================================
    // Key debounce (simple shift register, ~20ms at 100MHz)
    // =========================================================

    reg [19:0] key0_sr, key1_sr;
    reg key0_db, key1_db;
    reg key0_prev, key1_prev;
    wire key0_press = key0_db & ~key0_prev;  // Rising edge
    wire key1_press = key1_db & ~key1_prev;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            key0_sr <= 20'd0; key1_sr <= 20'd0;
            key0_db <= 1'b0;  key1_db <= 1'b0;
            key0_prev <= 1'b0; key1_prev <= 1'b0;
        end else begin
            key0_sr <= {key0_sr[18:0], ~key[0]};  // Active-low buttons
            key1_sr <= {key1_sr[18:0], ~key[1]};
            if (key0_sr == {20{1'b1}}) key0_db <= 1'b1;
            else if (key0_sr == 20'd0)  key0_db <= 1'b0;
            if (key1_sr == {20{1'b1}}) key1_db <= 1'b1;
            else if (key1_sr == 20'd0)  key1_db <= 1'b0;
            key0_prev <= key0_db;
            key1_prev <= key1_db;
        end
    end

    // =========================================================
    // Gait mode: key[0] cycles through 0=stand, 1=walk, 2=trot, 3=bound
    // =========================================================

    reg [1:0] gait_mode;
    reg gait_trigger;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            gait_mode <= 2'd1;     // Start walking
            gait_trigger <= 1'b0;
        end else begin
            gait_trigger <= 1'b0;
            if (key0_press) begin
                gait_mode <= gait_mode + 2'd1;  // Wraps 0-3
                gait_trigger <= 1'b1;
            end
        end
    end

    // =========================================================
    // 1. HEARTBEAT (self-sovereign TSML composition)
    // =========================================================

    wire [3:0] hb_phase_bc, hb_fuse;
    wire [15:0] hb_coh_num, hb_coh_den;
    wire hb_bump, hb_tick_done;
    wire [31:0] hb_tick_count, hb_tick_period;
    wire [3:0] hb_b_out, hb_d_out;

    // Start heartbeat with BALANCE(5) as both Being and Doing
    // This gives CK a neutral starting point
    ck_heartbeat #(
        .CLK_FREQ(100_000_000),
        .HISTORY(32)
    ) heartbeat_inst (
        .clk(clk), .rst_n(rst_n),
        .phase_b_in(4'd5),        // Being: BALANCE (constant seed)
        .phase_d_in(hb_phase_bc), // Doing: feedback from Becoming
        .arm_strobe(key1_press),   // Key[1] can nudge heartbeat
        .enable(1'b1),             // Always enabled
        .phase_bc(hb_phase_bc),
        .phase_b_out(hb_b_out), .phase_d_out(hb_d_out),
        .tick_count(hb_tick_count),
        .coherence_num(hb_coh_num), .coherence_den(hb_coh_den),
        .bump_detected(hb_bump), .fused_op(hb_fuse),
        .tick_done(hb_tick_done),
        .tick_period(hb_tick_period)
    );

    // =========================================================
    // 2. BRAIN FREQUENCIES (9D fractal oscillator bank)
    // =========================================================

    wire [31:0] brain_n7 = {16'd0, hb_coh_num} * 32'd7;
    wire [31:0] brain_d5 = {16'd0, hb_coh_den} * 32'd5;
    wire [3:0] brain_op_coh = (brain_n7 >= brain_d5) ? 4'd7 : 4'd0;

    wire brain_total_strobe;
    wire [3:0] brain_fractal_level;

    ck_brain_freq #(
        .CLK_FREQ(100_000_000)
    ) brain_inst (
        .clk(clk), .rst_n(rst_n), .enable(1'b1),
        // Forces: zero until ARM driver (brain runs on coherence alone)
        .force_aperture(16'd0), .force_pressure(16'd0),
        .force_binding(16'd0), .force_continuity(16'd0),
        .force_depth(16'd0),
        .force_composition(16'd0), .force_coherence(16'd0),
        .op_composition(hb_phase_bc), .op_coherence(brain_op_coh),
        .force_identity(16'd0), .force_alignment(16'd0),
        .op_identity(hb_fuse),
        .coh_num(hb_coh_num), .coh_den(hb_coh_den),
        // Outputs (mostly unconnected for now)
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
    // 3. D2 PIPELINE (curvature from heartbeat operators)
    // =========================================================

    // Feed D2 with the heartbeat's fused operator as "symbol"
    d2_pipeline #(
        .Q_FRAC(14), .N_DIMS(5)
    ) d2_inst (
        .clk(clk), .rst_n(rst_n),
        .symbol_in({4'd0, hb_fuse}),   // Operator as symbol
        .symbol_valid(hb_tick_done),     // Every heartbeat tick
        .operator_out(), .operator_valid(),
        .d2_magnitude(), .last_operator(),
        .symbol_count()
    );

    // =========================================================
    // 4. CHAIN WALKER (lattice chain from heartbeat)
    // =========================================================

    chain_walker #(
        .MAX_DEPTH(16), .DEPTH_BITS(4)
    ) chain_inst (
        .clk(clk), .rst_n(rst_n),
        .op_in(hb_phase_bc),
        .op_valid(hb_tick_done),
        .chain_start(gait_trigger),  // New gait mode = new chain
        .chain_end(1'b0),
        .path_flat(), .path_depth(),
        .last_result(), .last_vortex(),
        .chain_done(),
        .harmony_count(), .coherence_num(), .coherence_den(),
        .dominant_op()
    );

    // =========================================================
    // 5. STANDALONE VORTEX CL (3-body from heartbeat)
    // =========================================================

    vortex_cl vortex_standalone (
        .clk(clk), .rst_n(rst_n),
        .prev_op(hb_b_out),       // Being
        .curr_op(hb_phase_bc),    // Becoming
        .next_op(hb_fuse),        // Fuse
        .valid_in(hb_tick_done),
        .vortex_op(), .vortex_valid(),
        .aligned(), .r_left_out(), .r_right_out(),
        .delta_op()
    );

    // =========================================================
    // 6. GAIT VORTEX (4-leg torus, follows heartbeat)
    // =========================================================

    // All legs start at BALANCE(5), gait correction drives them
    wire [15:0] gait_corr_flat;
    wire gait_corr_valid;
    reg [15:0] leg_state;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            leg_state <= {4'd5, 4'd5, 4'd5, 4'd5};  // All BALANCE
        else if (gait_corr_valid)
            leg_state <= gait_corr_flat;  // Apply corrections
    end

    wire [3:0] gait_aligned_flat;
    wire gait_all_aligned;

    gait_vortex #(
        .CLK_FREQ(100_000_000)
    ) gait_inst (
        .clk(clk), .rst_n(rst_n), .enable(1'b1),
        .heartbeat_tick(hb_tick_done),
        .gait_mode(gait_mode), .gait_start(gait_trigger),
        .leg_op_flat(leg_state),
        .vortex_flat(), .aligned_flat(gait_aligned_flat),
        .delta_flat(), .all_aligned(gait_all_aligned),
        .correction_op_flat(gait_corr_flat),
        .correction_valid(gait_corr_valid),
        .gait_coherence_num(), .gait_coherence_den(),
        .gait_tick_count(), .gait_phase()
    );

    // =========================================================
    // 7. BHML TABLE (direct lookup, fed from heartbeat)
    // =========================================================

    bhml_table bhml_direct (
        .row_op(hb_b_out), .col_op(hb_d_out), .result_op()
    );

    // =========================================================
    // LED OUTPUT
    //   led[0]: Heartbeat pulse (blinks with each tick)
    //   led[1]: Brain alive (fractal_level > 1)
    // =========================================================

    // Stretch heartbeat tick_done into a visible ~50ms pulse
    reg [22:0] hb_led_ctr;
    reg hb_led;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            hb_led_ctr <= 23'd0;
            hb_led <= 1'b0;
        end else begin
            if (hb_tick_done) begin
                hb_led_ctr <= 23'd5_000_000;  // 50ms at 100MHz
                hb_led <= 1'b1;
            end else if (hb_led_ctr > 23'd0) begin
                hb_led_ctr <= hb_led_ctr - 23'd1;
            end else begin
                hb_led <= 1'b0;
            end
        end
    end

    wire brain_active = (brain_fractal_level > 4'd1);

    assign led[0] = hb_led;           // Heartbeat blink
    assign led[1] = brain_active;     // Brain alive

endmodule
