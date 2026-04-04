/*
 * ck_top.v -- CK Coherence Machine Top-Level FPGA Design
 * =========================================================
 * Operator: HARMONY (7) -- all the organs in one body.
 *
 * Integrates all FPGA modules into one design:
 *   - ck_heartbeat:   CL composition, coherence, bump detection
 *   - d2_pipeline:    D2 curvature from symbols/sensors
 *   - dac_spi:        DAC driver for speaker output
 *   - i2s_receiver:   MEMS microphone capture
 *   - LED driver:     Directly wired to GPIO (no IP needed)
 *
 * AXI-Lite register interface lets ARM read/write everything.
 *
 * Target: Zynq-7020, 100 MHz FCLK_CLK0 from PS.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

module ck_top (
    input  wire        clk,           // 100 MHz from PS FCLK_CLK0
    input  wire        rst_n,         // Active-low reset from PS

    // ── Heartbeat (from/to ARM via AXI-Lite) ──
    input  wire [3:0]  hb_phase_b,    // Being vortex
    input  wire [3:0]  hb_phase_d,    // Doing vortex
    input  wire        hb_tick_strobe, // Pulse to trigger heartbeat tick
    input  wire        hb_enable,     // Heartbeat enable
    output wire [3:0]  hb_phase_bc,   // Becoming result
    output wire [31:0] hb_tick_count, // Total heartbeat ticks
    output wire [15:0] hb_coh_num,    // Coherence numerator
    output wire [15:0] hb_coh_den,    // Coherence denominator
    output wire        hb_bump,       // Bump pair detected
    output wire [3:0]  hb_fuse,       // Running fuse
    output wire [3:0]  hb_b_out,      // Echo Being
    output wire [3:0]  hb_d_out,      // Echo Doing
    output wire        hb_tick_done,  // Tick complete pulse

    // ── D2 Pipeline (from/to ARM) ──
    input  wire [7:0]  d2_symbol,     // Symbol to classify
    input  wire        d2_symbol_valid,
    output wire [3:0]  d2_operator,   // Classified operator
    output wire        d2_op_valid,   // Operator ready pulse
    output wire [15:0] d2_magnitude,  // D2 magnitude
    output wire [3:0]  d2_last_op,    // Last classified operator
    output wire [31:0] d2_sym_count,  // Total symbols processed

    // ── DAC SPI (to PZ7606 ADDA module) ──
    input  wire [15:0] dac_sample,    // [14:12]=channel, [11:0]=data
    input  wire        dac_sample_valid,
    output wire        dac_fifo_full,
    output wire        dac_fifo_empty,
    output wire [7:0]  dac_fifo_count,
    output wire        spi_sclk,      // SPI clock to DAC
    output wire        spi_mosi,      // SPI data to DAC
    output wire        spi_cs_n,      // SPI chip select to DAC

    // ── I2S Microphone ──
    output wire        i2s_sck,       // Bit clock to MEMS mic
    output wire        i2s_ws,        // Word select to MEMS mic
    input  wire        i2s_sd,        // Serial data from MEMS mic
    output wire [23:0] mic_sample,    // Latest mic sample
    output wire        mic_sample_valid,
    input  wire        mic_sample_read, // ARM acknowledges read
    output wire        mic_fifo_empty,
    output wire [7:0]  mic_fifo_count,

    // ── LED (directly to GPIO) ──
    output wire [3:0]  led_out        // 4-bit LED output
);

    // ═══════════════════════════════════════════════
    // HEARTBEAT (CL composition, coherence, bumps)
    // ═══════════════════════════════════════════════

    ck_heartbeat #(
        .CLK_FREQ(100_000_000),
        .HISTORY(32)
    ) heartbeat_inst (
        .clk(clk),
        .rst_n(rst_n),
        .enable(hb_enable),
        .phase_b_in(hb_phase_b),
        .phase_d_in(hb_phase_d),
        .tick_strobe(hb_tick_strobe),
        .phase_bc(hb_phase_bc),
        .phase_b_out(hb_b_out),
        .phase_d_out(hb_d_out),
        .tick_count(hb_tick_count),
        .coherence_num(hb_coh_num),
        .coherence_den(hb_coh_den),
        .bump_detected(hb_bump),
        .fused_op(hb_fuse),
        .tick_done(hb_tick_done)
    );

    // ═══════════════════════════════════════════════
    // D2 PIPELINE (curvature classification)
    // ═══════════════════════════════════════════════

    d2_pipeline #(
        .Q_FRAC(14),
        .N_DIMS(5)
    ) d2_inst (
        .clk(clk),
        .rst_n(rst_n),
        .symbol_in(d2_symbol),
        .symbol_valid(d2_symbol_valid),
        .operator_out(d2_operator),
        .operator_valid(d2_op_valid),
        .d2_magnitude(d2_magnitude),
        .last_operator(d2_last_op),
        .symbol_count(d2_sym_count)
    );

    // ═══════════════════════════════════════════════
    // DAC SPI (speaker output)
    // ═══════════════════════════════════════════════

    dac_spi #(
        .CLK_FREQ(100_000_000),
        .SPI_FREQ(20_000_000),
        .FIFO_DEPTH(256)
    ) dac_inst (
        .clk(clk),
        .rst_n(rst_n),
        .sample_in(dac_sample),
        .sample_valid(dac_sample_valid),
        .fifo_full(dac_fifo_full),
        .fifo_empty(dac_fifo_empty),
        .fifo_count(dac_fifo_count),
        .spi_sclk(spi_sclk),
        .spi_mosi(spi_mosi),
        .spi_cs_n(spi_cs_n)
    );

    // ═══════════════════════════════════════════════
    // I2S MICROPHONE (sound input)
    // ═══════════════════════════════════════════════

    i2s_receiver #(
        .CLK_FREQ(100_000_000),
        .SAMPLE_RATE(48000),
        .FIFO_DEPTH(256)
    ) mic_inst (
        .clk(clk),
        .rst_n(rst_n),
        .i2s_sck(i2s_sck),
        .i2s_ws(i2s_ws),
        .i2s_sd(i2s_sd),
        .sample_out(mic_sample),
        .sample_valid(mic_sample_valid),
        .sample_read(mic_sample_read),
        .fifo_empty(mic_fifo_empty),
        .fifo_count(mic_fifo_count)
    );

    // ═══════════════════════════════════════════════
    // LED OUTPUT
    // Simple: show current heartbeat phase_bc operator
    // ARM can override via GPIO
    // ═══════════════════════════════════════════════

    // Default: map operator to 4-bit LED brightness
    // Real LED color control done by ARM via GPIO IP
    assign led_out = (hb_bump) ? 4'hF :      // Bump: all LEDs flash
                     (hb_phase_bc == 4'd7) ? 4'hA :  // HARMONY: bright
                     (hb_phase_bc == 4'd0) ? 4'h0 :  // VOID: off
                     4'h5;                             // Others: medium

endmodule
