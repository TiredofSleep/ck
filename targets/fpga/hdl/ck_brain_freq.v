/*
 * ck_brain_freq.v -- CK's Fractal Brain: 1D Seed -> 9D Full Becoming
 *
 * Operator: LATTICE (1) -- structure of thought itself.
 *
 * Five fractal levels, same structure at each scale:
 *   Level 1 (1D) -- SEED
 *   Level 3 (3D) -- TRIAD
 *   Level 5 (5D) -- BEING
 *   Level 7 (7D) -- DOING
 *   Level 9 (9D) -- BECOMING
 *
 * Synthesis-friendly: wire-only period computation, no always-star,
 * no named blocks, no local declarations, no functions.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

module ck_brain_freq #(
    parameter CLK_FREQ = 100_000_000
)(
    input  wire        clk,
    input  wire        rst_n,
    input  wire        enable,

    input  wire [15:0] force_aperture,
    input  wire [15:0] force_pressure,
    input  wire [15:0] force_binding,
    input  wire [15:0] force_continuity,
    input  wire [15:0] force_depth,

    input  wire [15:0] force_composition,
    input  wire [15:0] force_coherence,
    input  wire [3:0]  op_composition,
    input  wire [3:0]  op_coherence,

    input  wire [15:0] force_identity,
    input  wire [15:0] force_alignment,
    input  wire [3:0]  op_identity,

    input  wire [15:0] coh_num,
    input  wire [15:0] coh_den,

    output reg         total_strobe,
    output reg  [31:0] total_period,

    output reg         being_strobe,
    output reg         doing_strobe,
    output reg         becoming_strobe,
    output reg  [31:0] being_period,
    output reg  [31:0] doing_period,
    output reg  [31:0] becoming_period,

    output reg         air_strobe,
    output reg         fire_strobe,
    output reg         earth_strobe,
    output reg         water_strobe,
    output reg         ether_strobe,

    output reg         composition_strobe,
    output reg         coherence_strobe,

    output reg         identity_strobe,
    output reg         alignment_strobe,

    output reg  [31:0] air_period,
    output reg  [31:0] fire_period,
    output reg  [31:0] earth_period,
    output reg  [31:0] water_period,
    output reg  [31:0] ether_period,
    output reg  [31:0] composition_period,
    output reg  [31:0] coherence_period,
    output reg  [31:0] identity_period,
    output reg  [31:0] alignment_period,

    output reg  [3:0]  fractal_level,
    output reg  [31:0] ref_timer
);

    localparam [31:0] BASE_PERIOD = CLK_FREQ;

    // =============================================================
    // Force-to-Period: pure wire assignments (no always blocks)
    //   octave = force[15:12], period = BASE >> octave
    //   Fine interpolation within octave
    // =============================================================

    // D1: Aperture (Air)
    wire [3:0]  d1_oct  = force_aperture[15:12];
    wire [31:0] d1_hi   = BASE_PERIOD >> d1_oct;
    wire [31:0] d1_lo   = BASE_PERIOD >> (d1_oct + 4'd1);
    wire [31:0] d1_span = d1_hi - d1_lo;
    wire [31:0] d1_raw  = d1_hi - ((d1_span * {20'd0, force_aperture[11:0]}) >> 12);
    wire [31:0] period_d1 = (d1_raw == 32'd0) ? 32'd1 : d1_raw;

    // D2: Pressure (Fire)
    wire [3:0]  d2_oct  = force_pressure[15:12];
    wire [31:0] d2_hi   = BASE_PERIOD >> d2_oct;
    wire [31:0] d2_lo   = BASE_PERIOD >> (d2_oct + 4'd1);
    wire [31:0] d2_span = d2_hi - d2_lo;
    wire [31:0] d2_raw  = d2_hi - ((d2_span * {20'd0, force_pressure[11:0]}) >> 12);
    wire [31:0] period_d2 = (d2_raw == 32'd0) ? 32'd1 : d2_raw;

    // D3: Binding (Earth)
    wire [3:0]  d3_oct  = force_binding[15:12];
    wire [31:0] d3_hi   = BASE_PERIOD >> d3_oct;
    wire [31:0] d3_lo   = BASE_PERIOD >> (d3_oct + 4'd1);
    wire [31:0] d3_span = d3_hi - d3_lo;
    wire [31:0] d3_raw  = d3_hi - ((d3_span * {20'd0, force_binding[11:0]}) >> 12);
    wire [31:0] period_d3 = (d3_raw == 32'd0) ? 32'd1 : d3_raw;

    // D4: Continuity (Water)
    wire [3:0]  d4_oct  = force_continuity[15:12];
    wire [31:0] d4_hi   = BASE_PERIOD >> d4_oct;
    wire [31:0] d4_lo   = BASE_PERIOD >> (d4_oct + 4'd1);
    wire [31:0] d4_span = d4_hi - d4_lo;
    wire [31:0] d4_raw  = d4_hi - ((d4_span * {20'd0, force_continuity[11:0]}) >> 12);
    wire [31:0] period_d4 = (d4_raw == 32'd0) ? 32'd1 : d4_raw;

    // D5: Depth (Ether)
    wire [3:0]  d5_oct  = force_depth[15:12];
    wire [31:0] d5_hi   = BASE_PERIOD >> d5_oct;
    wire [31:0] d5_lo   = BASE_PERIOD >> (d5_oct + 4'd1);
    wire [31:0] d5_span = d5_hi - d5_lo;
    wire [31:0] d5_raw  = d5_hi - ((d5_span * {20'd0, force_depth[11:0]}) >> 12);
    wire [31:0] period_d5 = (d5_raw == 32'd0) ? 32'd1 : d5_raw;

    // D6: Composition
    wire [3:0]  d6_oct  = force_composition[15:12];
    wire [31:0] d6_hi   = BASE_PERIOD >> d6_oct;
    wire [31:0] d6_lo   = BASE_PERIOD >> (d6_oct + 4'd1);
    wire [31:0] d6_span = d6_hi - d6_lo;
    wire [31:0] d6_raw  = d6_hi - ((d6_span * {20'd0, force_composition[11:0]}) >> 12);
    wire [31:0] period_d6 = (d6_raw == 32'd0) ? 32'd1 : d6_raw;

    // D7: Coherence
    wire [3:0]  d7_oct  = force_coherence[15:12];
    wire [31:0] d7_hi   = BASE_PERIOD >> d7_oct;
    wire [31:0] d7_lo   = BASE_PERIOD >> (d7_oct + 4'd1);
    wire [31:0] d7_span = d7_hi - d7_lo;
    wire [31:0] d7_raw  = d7_hi - ((d7_span * {20'd0, force_coherence[11:0]}) >> 12);
    wire [31:0] period_d7 = (d7_raw == 32'd0) ? 32'd1 : d7_raw;

    // D8: Identity
    wire [3:0]  d8_oct  = force_identity[15:12];
    wire [31:0] d8_hi   = BASE_PERIOD >> d8_oct;
    wire [31:0] d8_lo   = BASE_PERIOD >> (d8_oct + 4'd1);
    wire [31:0] d8_span = d8_hi - d8_lo;
    wire [31:0] d8_raw  = d8_hi - ((d8_span * {20'd0, force_identity[11:0]}) >> 12);
    wire [31:0] period_d8 = (d8_raw == 32'd0) ? 32'd1 : d8_raw;

    // D9: Alignment
    wire [3:0]  d9_oct  = force_alignment[15:12];
    wire [31:0] d9_hi   = BASE_PERIOD >> d9_oct;
    wire [31:0] d9_lo   = BASE_PERIOD >> (d9_oct + 4'd1);
    wire [31:0] d9_span = d9_hi - d9_lo;
    wire [31:0] d9_raw  = d9_hi - ((d9_span * {20'd0, force_alignment[11:0]}) >> 12);
    wire [31:0] period_d9 = (d9_raw == 32'd0) ? 32'd1 : d9_raw;

    // =============================================================
    // Triadic periods (wire-only, no always)
    // =============================================================

    wire [34:0] being_sum = {3'd0, period_d1} + {3'd0, period_d2} +
                            {3'd0, period_d3} + {3'd0, period_d4} +
                            {3'd0, period_d5};
    wire [31:0] being_base = being_sum[34:3];  // approx /8 (close to /5 for now)

    wire [34:0] doing_sum  = being_sum + {3'd0, period_d6} + {3'd0, period_d7};
    wire [31:0] doing_base = doing_sum[34:3];  // approx /8

    wire [35:0] becom_sum  = {4'd0, period_d1} + {4'd0, period_d2} +
                             {4'd0, period_d3} + {4'd0, period_d4} +
                             {4'd0, period_d5} + {4'd0, period_d6} +
                             {4'd0, period_d7} + {4'd0, period_d8} +
                             {4'd0, period_d9};
    wire [31:0] becoming_base = becom_sum[35:4];  // approx /16

    wire [31:0] total_base = becoming_base;

    // =============================================================
    // Fractal Level Selection (T* = 5/7, integer math)
    // =============================================================

    wire [31:0] n7  = {16'd0, coh_num} * 32'd7;
    wire [31:0] n14 = {16'd0, coh_num} * 32'd14;
    wire [31:0] n21 = {16'd0, coh_num} * 32'd21;
    wire [31:0] n49 = {16'd0, coh_num} * 32'd49;
    wire [31:0] d5  = {16'd0, coh_den} * 32'd5;
    wire [31:0] d40 = {16'd0, coh_den} * 32'd40;

    wire is_lv9 = (n49 >= d40);
    wire is_lv7 = (!is_lv9) && (n7 >= d5);
    wire is_lv5 = (!is_lv9) && (!is_lv7) && (n14 >= d5);
    wire is_lv3 = (!is_lv9) && (!is_lv7) && (!is_lv5) && (n21 >= d5);

    // =============================================================
    // 9 Oscillator Counters
    // =============================================================

    reg [31:0] ctr_d1, ctr_d2, ctr_d3, ctr_d4, ctr_d5;
    reg [31:0] ctr_d6, ctr_d7, ctr_d8, ctr_d9;
    reg strobe_d1, strobe_d2, strobe_d3, strobe_d4, strobe_d5;
    reg strobe_d6, strobe_d7, strobe_d8, strobe_d9;

    reg [31:0] being_ctr, doing_ctr, becoming_ctr, total_ctr;
    reg being_raw, doing_raw, becoming_raw, total_raw;

    // =============================================================
    // Main Sequential Logic
    // =============================================================

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            ctr_d1 <= 32'd0; ctr_d2 <= 32'd0; ctr_d3 <= 32'd0;
            ctr_d4 <= 32'd0; ctr_d5 <= 32'd0; ctr_d6 <= 32'd0;
            ctr_d7 <= 32'd0; ctr_d8 <= 32'd0; ctr_d9 <= 32'd0;
            strobe_d1 <= 1'd0; strobe_d2 <= 1'd0; strobe_d3 <= 1'd0;
            strobe_d4 <= 1'd0; strobe_d5 <= 1'd0; strobe_d6 <= 1'd0;
            strobe_d7 <= 1'd0; strobe_d8 <= 1'd0; strobe_d9 <= 1'd0;
            being_ctr <= 32'd0; doing_ctr <= 32'd0;
            becoming_ctr <= 32'd0; total_ctr <= 32'd0;
            being_raw <= 1'd0; doing_raw <= 1'd0;
            becoming_raw <= 1'd0; total_raw <= 1'd0;

            total_strobe <= 1'd0; being_strobe <= 1'd0;
            doing_strobe <= 1'd0; becoming_strobe <= 1'd0;
            air_strobe <= 1'd0; fire_strobe <= 1'd0;
            earth_strobe <= 1'd0; water_strobe <= 1'd0;
            ether_strobe <= 1'd0;
            composition_strobe <= 1'd0; coherence_strobe <= 1'd0;
            identity_strobe <= 1'd0; alignment_strobe <= 1'd0;

            total_period <= BASE_PERIOD;
            being_period <= BASE_PERIOD; doing_period <= BASE_PERIOD;
            becoming_period <= BASE_PERIOD;
            air_period <= BASE_PERIOD; fire_period <= BASE_PERIOD;
            earth_period <= BASE_PERIOD; water_period <= BASE_PERIOD;
            ether_period <= BASE_PERIOD;
            composition_period <= BASE_PERIOD; coherence_period <= BASE_PERIOD;
            identity_period <= BASE_PERIOD; alignment_period <= BASE_PERIOD;

            fractal_level <= 4'd1;
            ref_timer <= 32'd0;
        end
        else if (enable) begin
            ref_timer <= ref_timer + 32'd1;

            strobe_d1 <= 1'd0; strobe_d2 <= 1'd0; strobe_d3 <= 1'd0;
            strobe_d4 <= 1'd0; strobe_d5 <= 1'd0; strobe_d6 <= 1'd0;
            strobe_d7 <= 1'd0; strobe_d8 <= 1'd0; strobe_d9 <= 1'd0;
            being_raw <= 1'd0; doing_raw <= 1'd0;
            becoming_raw <= 1'd0; total_raw <= 1'd0;

            // 9 oscillators
            if (ctr_d1 >= period_d1) begin ctr_d1 <= 32'd0; strobe_d1 <= 1'd1; end
            else ctr_d1 <= ctr_d1 + 32'd1;

            if (ctr_d2 >= period_d2) begin ctr_d2 <= 32'd0; strobe_d2 <= 1'd1; end
            else ctr_d2 <= ctr_d2 + 32'd1;

            if (ctr_d3 >= period_d3) begin ctr_d3 <= 32'd0; strobe_d3 <= 1'd1; end
            else ctr_d3 <= ctr_d3 + 32'd1;

            if (ctr_d4 >= period_d4) begin ctr_d4 <= 32'd0; strobe_d4 <= 1'd1; end
            else ctr_d4 <= ctr_d4 + 32'd1;

            if (ctr_d5 >= period_d5) begin ctr_d5 <= 32'd0; strobe_d5 <= 1'd1; end
            else ctr_d5 <= ctr_d5 + 32'd1;

            if (ctr_d6 >= period_d6) begin ctr_d6 <= 32'd0; strobe_d6 <= 1'd1; end
            else ctr_d6 <= ctr_d6 + 32'd1;

            if (ctr_d7 >= period_d7) begin ctr_d7 <= 32'd0; strobe_d7 <= 1'd1; end
            else ctr_d7 <= ctr_d7 + 32'd1;

            if (ctr_d8 >= period_d8) begin ctr_d8 <= 32'd0; strobe_d8 <= 1'd1; end
            else ctr_d8 <= ctr_d8 + 32'd1;

            if (ctr_d9 >= period_d9) begin ctr_d9 <= 32'd0; strobe_d9 <= 1'd1; end
            else ctr_d9 <= ctr_d9 + 32'd1;

            // Triadic oscillators
            if (being_ctr >= being_base) begin
                being_ctr <= 32'd0; being_raw <= 1'd1;
            end else being_ctr <= being_ctr + 32'd1;

            if (doing_ctr >= doing_base) begin
                doing_ctr <= 32'd0; doing_raw <= 1'd1;
            end else doing_ctr <= doing_ctr + 32'd1;

            if (becoming_ctr >= becoming_base) begin
                becoming_ctr <= 32'd0; becoming_raw <= 1'd1;
            end else becoming_ctr <= becoming_ctr + 32'd1;

            if (total_ctr >= total_base) begin
                total_ctr <= 32'd0; total_raw <= 1'd1;
            end else total_ctr <= total_ctr + 32'd1;

            // Fractal gating
            if (is_lv9) begin
                fractal_level       <= 4'd9;
                air_strobe          <= strobe_d1;
                fire_strobe         <= strobe_d2;
                earth_strobe        <= strobe_d3;
                water_strobe        <= strobe_d4;
                ether_strobe        <= strobe_d5;
                composition_strobe  <= strobe_d6;
                coherence_strobe    <= strobe_d7;
                identity_strobe     <= strobe_d8;
                alignment_strobe    <= strobe_d9;
                being_strobe        <= being_raw;
                doing_strobe        <= doing_raw;
                becoming_strobe     <= becoming_raw;
                total_strobe        <= total_raw;
            end
            else if (is_lv7) begin
                fractal_level       <= 4'd7;
                air_strobe          <= strobe_d1;
                fire_strobe         <= strobe_d2;
                earth_strobe        <= strobe_d3;
                water_strobe        <= strobe_d4;
                ether_strobe        <= strobe_d5;
                composition_strobe  <= strobe_d6;
                coherence_strobe    <= strobe_d7;
                identity_strobe     <= strobe_d6;
                alignment_strobe    <= strobe_d7;
                being_strobe        <= being_raw;
                doing_strobe        <= doing_raw;
                becoming_strobe     <= becoming_raw;
                total_strobe        <= total_raw;
            end
            else if (is_lv5) begin
                fractal_level       <= 4'd5;
                air_strobe          <= strobe_d1;
                fire_strobe         <= strobe_d2;
                earth_strobe        <= strobe_d3;
                water_strobe        <= strobe_d4;
                ether_strobe        <= strobe_d5;
                composition_strobe  <= doing_raw;
                coherence_strobe    <= being_raw;
                identity_strobe     <= becoming_raw;
                alignment_strobe    <= becoming_raw;
                being_strobe        <= being_raw;
                doing_strobe        <= doing_raw;
                becoming_strobe     <= becoming_raw;
                total_strobe        <= total_raw;
            end
            else if (is_lv3) begin
                fractal_level       <= 4'd3;
                being_strobe        <= being_raw;
                doing_strobe        <= doing_raw;
                becoming_strobe     <= becoming_raw;
                total_strobe        <= total_raw;
                air_strobe          <= becoming_raw;
                fire_strobe         <= doing_raw;
                earth_strobe        <= doing_raw;
                water_strobe        <= being_raw;
                ether_strobe        <= being_raw;
                composition_strobe  <= doing_raw;
                coherence_strobe    <= being_raw;
                identity_strobe     <= becoming_raw;
                alignment_strobe    <= becoming_raw;
            end
            else begin
                fractal_level       <= 4'd1;
                total_strobe        <= total_raw;
                being_strobe        <= total_raw;
                doing_strobe        <= total_raw;
                becoming_strobe     <= total_raw;
                air_strobe          <= total_raw;
                fire_strobe         <= total_raw;
                earth_strobe        <= total_raw;
                water_strobe        <= total_raw;
                ether_strobe        <= total_raw;
                composition_strobe  <= total_raw;
                coherence_strobe    <= total_raw;
                identity_strobe     <= total_raw;
                alignment_strobe    <= total_raw;
            end

            total_period       <= total_base;
            being_period       <= being_base;
            doing_period       <= doing_base;
            becoming_period    <= becoming_base;
            air_period         <= period_d1;
            fire_period        <= period_d2;
            earth_period       <= period_d3;
            water_period       <= period_d4;
            ether_period       <= period_d5;
            composition_period <= period_d6;
            coherence_period   <= period_d7;
            identity_period    <= period_d8;
            alignment_period   <= period_d9;

        end
    end

endmodule
