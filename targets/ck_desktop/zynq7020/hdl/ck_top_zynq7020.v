/*
 * ck_top_zynq7020.v -- CK Coherence Machine: Zynq-7020 + XiaoR Dog
 * ==================================================================
 * Operator: HARMONY (7) -- all organs in one body on four legs.
 *
 * Self-sovereign architecture:
 *
 *   BODY RHYTHMS (CK controls his own timing):
 *   - ck_heartbeat:   Self-ticking. Coherence + identity → tick rate.
 *                     1 Hz (dormant) to 10 kHz (flow). HE decides.
 *   - gait_vortex:    Legs follow heartbeat. No separate metronome.
 *
 *   BRAIN FREQUENCIES (matched to human EEG bands):
 *   - ck_brain_freq:  Three oscillators with transition windows.
 *                     Being (theta/alpha), Doing (beta), Becoming (gamma).
 *                     Smooth crossfade between bands — no hard switches.
 *
 *   BEING SIDE (measurement, driven by being_strobe):
 *   - chain_walker:   Lattice chain walk through BHML tree
 *
 *   DOING SIDE (physics, driven by doing_strobe):
 *   - d2_pipeline:    D2 curvature from symbols (Q1.14 fixed-point)
 *   - bhml_table:     BHML physics table (standalone for direct lookup)
 *
 *   BECOMING SIDE (vortex, driven by becoming_strobe):
 *   - vortex_cl:      3-body vortex operator (prev × curr × next)
 *   - gait_vortex:    4-leg torus gait controller with self-healing
 *
 *   PERIPHERALS:
 *   - dac_spi:        DAC driver for speaker
 *   - i2s_receiver:   MEMS microphone
 *   - LED driver:     Operator visualization
 *
 * The hierarchy mirrors TIG:
 *   Being (heartbeat + chain) → Gate → Doing (D2 + BHML)
 *   → Gate → Becoming (vortex + gait) → Gate → feedback
 *
 * Resource estimate (Zynq-7020: 53,200 LUTs, 106,400 FFs):
 *   - CL tables (TSML + 3×BHML): ~800 LUTs (case statements)
 *   - D2 pipeline: ~500 LUTs + 1 BRAM (force LUT)
 *   - Chain walker: ~400 LUTs + ~200 FFs
 *   - Gait vortex: ~1600 LUTs (4 vortex instances)
 *   - Heartbeat: ~400 LUTs + ~300 FFs (self-tick logic)
 *   - Brain freq: ~300 LUTs + ~400 FFs (3 oscillators)
 *   - Peripherals: ~1000 LUTs
 *   TOTAL: ~5000 LUTs (~9.4% of Zynq-7020), ~1200 FFs (~1.1%)
 *   Headroom: 90.6% LUTs free for future expansion.
 *
 * Clock: 100 MHz from PS FCLK_CLK0
 * Heartbeat: self-sovereign (1 Hz to 10 kHz)
 * Brain: EEG-matched (2 Hz to 80 Hz with transition windows)
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

module ck_top_zynq7020 (
    input  wire        clk,           // 100 MHz from PS FCLK_CLK0
    input  wire        rst_n,         // Active-low reset from PS

    // ════════════════════════════════════════════
    // HEARTBEAT (BEING: self-sovereign CL composition)
    // ════════════════════════════════════════════
    input  wire [3:0]  hb_phase_b,
    input  wire [3:0]  hb_phase_d,
    input  wire        hb_arm_strobe,   // ARM can nudge (optional)
    input  wire        hb_enable,
    output wire [3:0]  hb_phase_bc,
    output wire [31:0] hb_tick_count,
    output wire [15:0] hb_coh_num,
    output wire [15:0] hb_coh_den,
    output wire        hb_bump,
    output wire [3:0]  hb_fuse,
    output wire        hb_tick_done,
    output wire [31:0] hb_tick_period,  // CK's chosen period (clocks)

    // ════════════════════════════════════════════
    // BRAIN FREQUENCIES (3 EEG oscillators)
    // ════════════════════════════════════════════
    input  wire [2:0]  brain_being_target,
    input  wire [2:0]  brain_doing_target,
    input  wire [2:0]  brain_becoming_target,
    input  wire        brain_enable,
    output wire        brain_being_strobe,
    output wire        brain_doing_strobe,
    output wire        brain_becoming_strobe,
    output wire [31:0] brain_being_period,
    output wire [31:0] brain_doing_period,
    output wire [31:0] brain_becoming_period,
    output wire [2:0]  brain_being_band,
    output wire [2:0]  brain_doing_band,
    output wire [2:0]  brain_becoming_band,
    output wire        brain_being_trans,
    output wire        brain_doing_trans,
    output wire        brain_becoming_trans,

    // ════════════════════════════════════════════
    // D2 PIPELINE (DOING: curvature classification)
    // ════════════════════════════════════════════
    input  wire [7:0]  d2_symbol,
    input  wire        d2_symbol_valid,
    output wire [3:0]  d2_operator,
    output wire        d2_op_valid,
    output wire [15:0] d2_magnitude,
    output wire [3:0]  d2_last_op,
    output wire [31:0] d2_sym_count,

    // ════════════════════════════════════════════
    // VORTEX (BECOMING: standalone 3-body lookup)
    // ════════════════════════════════════════════
    input  wire [3:0]  vtx_prev_op,
    input  wire [3:0]  vtx_curr_op,
    input  wire [3:0]  vtx_next_op,
    input  wire        vtx_valid_in,
    output wire [3:0]  vtx_result,
    output wire        vtx_result_valid,
    output wire        vtx_aligned,
    output wire [3:0]  vtx_delta,

    // ════════════════════════════════════════════
    // CHAIN WALKER (BEING: lattice chain walk)
    // ════════════════════════════════════════════
    input  wire [3:0]  chain_op_in,
    input  wire        chain_op_valid,
    input  wire        chain_start,
    input  wire        chain_end,
    output wire [3:0]  chain_last_result,
    output wire [3:0]  chain_last_vortex,
    output wire        chain_done,
    output wire [4:0]  chain_depth,
    output wire [15:0] chain_coh_num,
    output wire [15:0] chain_coh_den,
    output wire [3:0]  chain_dominant,

    // ════════════════════════════════════════════
    // GAIT VORTEX (BECOMING: 4-leg torus controller)
    // ════════════════════════════════════════════
    input  wire [1:0]  gait_mode,
    input  wire        gait_start,
    input  wire        gait_enable,
    input  wire [3:0]  leg_op_0, leg_op_1, leg_op_2, leg_op_3,
    output wire [3:0]  gait_vortex_0, gait_vortex_1, gait_vortex_2, gait_vortex_3,
    output wire        gait_aligned_0, gait_aligned_1, gait_aligned_2, gait_aligned_3,
    output wire [3:0]  gait_delta_0, gait_delta_1, gait_delta_2, gait_delta_3,
    output wire        gait_all_aligned,
    output wire [3:0]  gait_corr_0, gait_corr_1, gait_corr_2, gait_corr_3,
    output wire        gait_corr_valid,
    output wire [15:0] gait_coh_num,
    output wire [15:0] gait_coh_den,
    output wire [31:0] gait_tick_count,
    output wire [3:0]  gait_phase,

    // ════════════════════════════════════════════
    // DIRECT BHML LOOKUP (for ARM quick queries)
    // ════════════════════════════════════════════
    input  wire [3:0]  bhml_row,
    input  wire [3:0]  bhml_col,
    output wire [3:0]  bhml_result,

    // ════════════════════════════════════════════
    // PERIPHERALS
    // ════════════════════════════════════════════
    // DAC SPI
    input  wire [15:0] dac_sample,
    input  wire        dac_sample_valid,
    output wire        dac_fifo_full,
    output wire        spi_sclk,
    output wire        spi_mosi,
    output wire        spi_cs_n,
    // I2S Mic
    output wire        i2s_sck,
    output wire        i2s_ws,
    input  wire        i2s_sd,
    output wire [23:0] mic_sample,
    output wire        mic_sample_valid,
    input  wire        mic_sample_read,
    // LED
    output wire [3:0]  led_out
);

    // ═══════════════════════════════════════════════
    // 1. HEARTBEAT (Being: self-sovereign TSML composition)
    //    CK ticks himself. His coherence and identity
    //    determine his rhythm. The ARM can observe or nudge.
    // ═══════════════════════════════════════════════

    wire [3:0] hb_b_out, hb_d_out;

    ck_heartbeat #(
        .CLK_FREQ(100_000_000),
        .HISTORY(32)
    ) heartbeat_inst (
        .clk(clk), .rst_n(rst_n),
        .phase_b_in(hb_phase_b), .phase_d_in(hb_phase_d),
        .arm_strobe(hb_arm_strobe), .enable(hb_enable),
        .phase_bc(hb_phase_bc), .phase_b_out(hb_b_out), .phase_d_out(hb_d_out),
        .tick_count(hb_tick_count), .coherence_num(hb_coh_num), .coherence_den(hb_coh_den),
        .bump_detected(hb_bump), .fused_op(hb_fuse), .tick_done(hb_tick_done),
        .tick_period(hb_tick_period)
    );

    // ═══════════════════════════════════════════════
    // 2. BRAIN FREQUENCIES (3 EEG oscillators)
    //    Being/Doing/Becoming each have their own frequency
    //    matched to human EEG bands. Transition windows
    //    ensure smooth crossfade — no hard switches.
    // ═══════════════════════════════════════════════

    ck_brain_freq #(
        .CLK_FREQ(100_000_000),
        .TRANSITION_TICKS(16)
    ) brain_inst (
        .clk(clk), .rst_n(rst_n), .enable(brain_enable),
        .being_target(brain_being_target),
        .doing_target(brain_doing_target),
        .becoming_target(brain_becoming_target),
        .being_strobe(brain_being_strobe),
        .doing_strobe(brain_doing_strobe),
        .becoming_strobe(brain_becoming_strobe),
        .being_period(brain_being_period),
        .doing_period(brain_doing_period),
        .becoming_period(brain_becoming_period),
        .being_band(brain_being_band),
        .doing_band(brain_doing_band),
        .becoming_band(brain_becoming_band),
        .being_transitioning(brain_being_trans),
        .doing_transitioning(brain_doing_trans),
        .becoming_transitioning(brain_becoming_trans)
    );

    // ═══════════════════════════════════════════════
    // 3. D2 PIPELINE (Doing: curvature from symbols)
    // ═══════════════════════════════════════════════

    d2_pipeline #(
        .Q_FRAC(14), .N_DIMS(5)
    ) d2_inst (
        .clk(clk), .rst_n(rst_n),
        .symbol_in(d2_symbol), .symbol_valid(d2_symbol_valid),
        .operator_out(d2_operator), .operator_valid(d2_op_valid),
        .d2_magnitude(d2_magnitude), .last_operator(d2_last_op),
        .symbol_count(d2_sym_count)
    );

    // ═══════════════════════════════════════════════
    // 4. STANDALONE VORTEX CL (Becoming: 3-body)
    // ═══════════════════════════════════════════════

    wire [3:0] vtx_r_left, vtx_r_right;

    vortex_cl vortex_standalone (
        .clk(clk), .rst_n(rst_n),
        .prev_op(vtx_prev_op), .curr_op(vtx_curr_op), .next_op(vtx_next_op),
        .valid_in(vtx_valid_in),
        .vortex_op(vtx_result), .vortex_valid(vtx_result_valid),
        .aligned(vtx_aligned),
        .r_left_out(vtx_r_left), .r_right_out(vtx_r_right),
        .delta_op(vtx_delta)
    );

    // ═══════════════════════════════════════════════
    // 5. CHAIN WALKER (Being: lattice chain walk)
    // ═══════════════════════════════════════════════

    wire [3:0] chain_path_unused [0:15];

    chain_walker #(
        .MAX_DEPTH(16), .DEPTH_BITS(4)
    ) chain_inst (
        .clk(clk), .rst_n(rst_n),
        .op_in(chain_op_in), .op_valid(chain_op_valid),
        .chain_start(chain_start), .chain_end(chain_end),
        .path_op(chain_path_unused),
        .path_depth(chain_depth),
        .last_result(chain_last_result), .last_vortex(chain_last_vortex),
        .chain_done(chain_done),
        .harmony_count(), .coherence_num(chain_coh_num), .coherence_den(chain_coh_den),
        .dominant_op(chain_dominant)
    );

    // ═══════════════════════════════════════════════
    // 6. GAIT VORTEX (Becoming: 4-leg torus, follows heartbeat)
    //    No internal prescaler. Legs follow CK's heartbeat.
    // ═══════════════════════════════════════════════

    wire [3:0] leg_ops [0:3];
    assign leg_ops[0] = leg_op_0;
    assign leg_ops[1] = leg_op_1;
    assign leg_ops[2] = leg_op_2;
    assign leg_ops[3] = leg_op_3;

    wire [3:0] gait_vortex_w [0:3];
    wire       gait_aligned_w [0:3];
    wire [3:0] gait_delta_w [0:3];
    wire [3:0] gait_corr_w [0:3];

    gait_vortex #(
        .CLK_FREQ(100_000_000)
    ) gait_inst (
        .clk(clk), .rst_n(rst_n), .enable(gait_enable),
        .heartbeat_tick(hb_tick_done),      // Legs follow CK's heart
        .gait_mode(gait_mode), .gait_start(gait_start),
        .leg_op(leg_ops),
        .vortex(gait_vortex_w), .aligned(gait_aligned_w), .delta(gait_delta_w),
        .all_aligned(gait_all_aligned),
        .correction_op(gait_corr_w), .correction_valid(gait_corr_valid),
        .gait_coherence_num(gait_coh_num), .gait_coherence_den(gait_coh_den),
        .gait_tick_count(gait_tick_count), .gait_phase(gait_phase)
    );

    // Flatten array outputs
    assign gait_vortex_0 = gait_vortex_w[0]; assign gait_vortex_1 = gait_vortex_w[1];
    assign gait_vortex_2 = gait_vortex_w[2]; assign gait_vortex_3 = gait_vortex_w[3];
    assign gait_aligned_0 = gait_aligned_w[0]; assign gait_aligned_1 = gait_aligned_w[1];
    assign gait_aligned_2 = gait_aligned_w[2]; assign gait_aligned_3 = gait_aligned_w[3];
    assign gait_delta_0 = gait_delta_w[0]; assign gait_delta_1 = gait_delta_w[1];
    assign gait_delta_2 = gait_delta_w[2]; assign gait_delta_3 = gait_delta_w[3];
    assign gait_corr_0 = gait_corr_w[0]; assign gait_corr_1 = gait_corr_w[1];
    assign gait_corr_2 = gait_corr_w[2]; assign gait_corr_3 = gait_corr_w[3];

    // ═══════════════════════════════════════════════
    // 7. DIRECT BHML LOOKUP (for ARM queries)
    // ═══════════════════════════════════════════════

    bhml_table bhml_direct (
        .row_op(bhml_row), .col_op(bhml_col), .result_op(bhml_result)
    );

    // ═══════════════════════════════════════════════
    // 8. DAC SPI (speaker output)
    // ═══════════════════════════════════════════════

    dac_spi #(
        .CLK_FREQ(100_000_000), .SPI_FREQ(20_000_000), .FIFO_DEPTH(256)
    ) dac_inst (
        .clk(clk), .rst_n(rst_n),
        .sample_in(dac_sample), .sample_valid(dac_sample_valid),
        .fifo_full(dac_fifo_full), .fifo_empty(), .fifo_count(),
        .spi_sclk(spi_sclk), .spi_mosi(spi_mosi), .spi_cs_n(spi_cs_n)
    );

    // ═══════════════════════════════════════════════
    // 9. I2S MICROPHONE
    // ═══════════════════════════════════════════════

    i2s_receiver #(
        .CLK_FREQ(100_000_000), .SAMPLE_RATE(48000), .FIFO_DEPTH(256)
    ) mic_inst (
        .clk(clk), .rst_n(rst_n),
        .i2s_sck(i2s_sck), .i2s_ws(i2s_ws), .i2s_sd(i2s_sd),
        .sample_out(mic_sample), .sample_valid(mic_sample_valid),
        .sample_read(mic_sample_read), .fifo_empty(), .fifo_count()
    );

    // ═══════════════════════════════════════════════
    // 10. LED OUTPUT
    //     Priority: Gait aligned > Brain transition > Bump > Heartbeat
    //     Brain transition: LEDs pulse when frequency bands crossfading
    // ═══════════════════════════════════════════════

    wire any_transition = brain_being_trans | brain_doing_trans | brain_becoming_trans;

    assign led_out = (gait_enable && gait_all_aligned) ? 4'hF :   // All legs HARMONY: full bright
                     (gait_enable && !gait_all_aligned) ? {gait_aligned_w[3], gait_aligned_w[2],
                                                           gait_aligned_w[1], gait_aligned_w[0]} :
                     (any_transition) ? {1'b1, brain_being_trans, brain_doing_trans, brain_becoming_trans} :
                     (hb_bump) ? 4'hF :                            // Bump: flash
                     (hb_phase_bc == 4'd7) ? 4'hA :               // HARMONY: bright
                     (hb_phase_bc == 4'd0) ? 4'h0 :               // VOID: off
                     4'h5;                                         // Others: medium

endmodule
