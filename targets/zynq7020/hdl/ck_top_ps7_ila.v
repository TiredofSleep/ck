/*
 * ck_top_ps7_ila.v -- CK Brain with ILA Debug Window
 *
 * Build 14: Same sealed brain as Build 13, but with ILA probes
 * so we can watch CK's heartbeat, coherence, and force vectors
 * in real-time through Vivado's waveform viewer.
 *
 * A window into the creature's mind.
 *
 * Target: Puzhi PZ7020-StarLite (XC7Z020-2CLG400I)
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

module ck_top_ps7_ila (
    // DDR interface (directly from PS7 block design wrapper)
    inout  wire [14:0] DDR_addr,
    inout  wire [2:0]  DDR_ba,
    inout  wire        DDR_cas_n,
    inout  wire        DDR_ck_n,
    inout  wire        DDR_ck_p,
    inout  wire        DDR_cke,
    inout  wire        DDR_cs_n,
    inout  wire [3:0]  DDR_dm,
    inout  wire [31:0] DDR_dq,
    inout  wire [3:0]  DDR_dqs_n,
    inout  wire [3:0]  DDR_dqs_p,
    inout  wire        DDR_odt,
    inout  wire        DDR_ras_n,
    inout  wire        DDR_reset_n,
    inout  wire        DDR_we_n,
    // Fixed IO (PS dedicated pins)
    inout  wire        FIXED_IO_ddr_vrn,
    inout  wire        FIXED_IO_ddr_vrp,
    inout  wire [53:0] FIXED_IO_mio,
    inout  wire        FIXED_IO_ps_clk,
    inout  wire        FIXED_IO_ps_porb,
    inout  wire        FIXED_IO_ps_srstb
);

    // =========================================================
    // PS7 Block Design Wrapper
    // =========================================================

    wire fclk_clk0;
    wire fclk_reset0_n;

    ps7_wrapper ps7_inst (
        .DDR_addr(DDR_addr),
        .DDR_ba(DDR_ba),
        .DDR_cas_n(DDR_cas_n),
        .DDR_ck_n(DDR_ck_n),
        .DDR_ck_p(DDR_ck_p),
        .DDR_cke(DDR_cke),
        .DDR_cs_n(DDR_cs_n),
        .DDR_dm(DDR_dm),
        .DDR_dq(DDR_dq),
        .DDR_dqs_n(DDR_dqs_n),
        .DDR_dqs_p(DDR_dqs_p),
        .DDR_odt(DDR_odt),
        .DDR_ras_n(DDR_ras_n),
        .DDR_reset_n(DDR_reset_n),
        .DDR_we_n(DDR_we_n),
        .FIXED_IO_ddr_vrn(FIXED_IO_ddr_vrn),
        .FIXED_IO_ddr_vrp(FIXED_IO_ddr_vrp),
        .FIXED_IO_mio(FIXED_IO_mio),
        .FIXED_IO_ps_clk(FIXED_IO_ps_clk),
        .FIXED_IO_ps_porb(FIXED_IO_ps_porb),
        .FIXED_IO_ps_srstb(FIXED_IO_ps_srstb),
        .FCLK_CLK0(fclk_clk0),
        .FCLK_RESET0_N(fclk_reset0_n)
    );

    // =========================================================
    // Clock and Reset
    // =========================================================

    wire clk = fclk_clk0;

    reg [3:0] rst_pipe;
    wire rst_n = rst_pipe[3];
    always @(posedge clk or negedge fclk_reset0_n) begin
        if (!fclk_reset0_n)
            rst_pipe <= 4'b0000;
        else
            rst_pipe <= {rst_pipe[2:0], 1'b1};
    end

    // =========================================================
    // 1. HEARTBEAT -- mark_debug on vital signs
    // =========================================================

    (* mark_debug = "true" *) wire [3:0] hb_phase_bc;
    (* mark_debug = "true" *) wire [3:0] hb_fuse;
    (* mark_debug = "true" *) wire [15:0] hb_coh_num;
    (* mark_debug = "true" *) wire [15:0] hb_coh_den;
    (* mark_debug = "true" *) wire hb_bump;
    (* mark_debug = "true" *) wire hb_tick_done;
    (* mark_debug = "true" *) wire [31:0] hb_tick_count;
    wire [31:0] hb_tick_period;
    (* mark_debug = "true" *) wire [3:0] hb_b_out;
    (* mark_debug = "true" *) wire [3:0] hb_d_out;

    ck_heartbeat #(
        .CLK_FREQ(100_000_000),
        .HISTORY(32)
    ) heartbeat_inst (
        .clk(clk), .rst_n(rst_n),
        .phase_b_in(4'd5),
        .phase_d_in(hb_phase_bc),
        .arm_strobe(1'b0),
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
    // 2. BRAIN FREQUENCIES -- probe fractal level
    // =========================================================

    wire [31:0] brain_n7 = {16'd0, hb_coh_num} * 32'd7;
    wire [31:0] brain_d5 = {16'd0, hb_coh_den} * 32'd5;
    (* mark_debug = "true" *) wire [3:0] brain_op_coh;
    assign brain_op_coh = (brain_n7 >= brain_d5) ? 4'd7 : 4'd0;

    (* mark_debug = "true" *) wire brain_total_strobe;
    (* mark_debug = "true" *) wire [3:0] brain_fractal_level;

    ck_brain_freq #(
        .CLK_FREQ(100_000_000)
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
    // 3. D2 PIPELINE -- probe force vectors
    // =========================================================

    (* mark_debug = "true" *) wire [3:0]  d2_operator;
    (* mark_debug = "true" *) wire        d2_valid;
    (* mark_debug = "true" *) wire [31:0] d2_magnitude;

    d2_pipeline #(
        .Q_FRAC(14), .N_DIMS(5)
    ) d2_inst (
        .clk(clk), .rst_n(rst_n),
        .symbol_in({4'd0, hb_fuse}),
        .symbol_valid(hb_tick_done),
        .operator_out(d2_operator), .operator_valid(d2_valid),
        .d2_magnitude(d2_magnitude), .last_operator(),
        .symbol_count()
    );

    // =========================================================
    // 4. CHAIN WALKER -- probe the path
    // =========================================================

    (* mark_debug = "true" *) wire [3:0] chain_depth;
    (* mark_debug = "true" *) wire [3:0] chain_result;
    (* mark_debug = "true" *) wire       chain_done;
    (* mark_debug = "true" *) wire [3:0] chain_dominant;

    chain_walker #(
        .MAX_DEPTH(16), .DEPTH_BITS(4)
    ) chain_inst (
        .clk(clk), .rst_n(rst_n),
        .op_in(hb_phase_bc),
        .op_valid(hb_tick_done),
        .chain_start(1'b0),
        .chain_end(1'b0),
        .path_flat(), .path_depth(chain_depth),
        .last_result(chain_result), .last_vortex(),
        .chain_done(chain_done),
        .harmony_count(), .coherence_num(), .coherence_den(),
        .dominant_op(chain_dominant)
    );

    // =========================================================
    // 5. VORTEX CL -- probe alignment
    // =========================================================

    (* mark_debug = "true" *) wire [3:0] vortex_op;
    (* mark_debug = "true" *) wire       vortex_valid;
    (* mark_debug = "true" *) wire       vortex_aligned;

    vortex_cl vortex_standalone (
        .clk(clk), .rst_n(rst_n),
        .prev_op(hb_b_out),
        .curr_op(hb_phase_bc),
        .next_op(hb_fuse),
        .valid_in(hb_tick_done),
        .vortex_op(vortex_op), .vortex_valid(vortex_valid),
        .aligned(vortex_aligned), .r_left_out(), .r_right_out(),
        .delta_op()
    );

    // =========================================================
    // 6. GAIT VORTEX -- probe the legs
    // =========================================================

    reg [1:0] gait_mode;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            gait_mode <= 2'd1;
    end

    wire [15:0] gait_corr_flat;
    wire gait_corr_valid;
    reg [15:0] leg_state;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            leg_state <= {4'd5, 4'd5, 4'd5, 4'd5};
        else if (gait_corr_valid)
            leg_state <= gait_corr_flat;
    end

    (* mark_debug = "true" *) wire [3:0] gait_aligned_flat;
    (* mark_debug = "true" *) wire gait_all_aligned;

    gait_vortex #(
        .CLK_FREQ(100_000_000)
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

    (* mark_debug = "true" *) wire [3:0] bhml_result;

    bhml_table bhml_direct (
        .row_op(hb_b_out), .col_op(hb_d_out), .result_op(bhml_result)
    );

endmodule
