/*
 * d2_clay.v -- D2 Curvature Engine for Clay Force Vectors
 * ========================================================
 *
 * Same D2 math as d2_pipeline.v, but accepts raw 5D Q1.14
 * force vectors directly (no ASCII-to-Hebrew-root LUT).
 *
 * Pipeline (2 stages):
 *   Stage 1: Shift history + compute D2 (v0 - 2*v1 + v2)
 *   Stage 2: Classify (argmax |D2|, sign -> operator)
 *
 * Uses 18-bit signed intermediates to prevent overflow.
 * Q1.14 input range: [0, 16384] for Clay (forces in [0,1]).
 * Max D2 = 16384 - 0 + 16384 = 32768 (overflows 16-bit).
 * 18-bit handles up to +/-131072.
 *
 * Operator map (same as d2_pipeline.v):
 *   aperture+  = CHAOS(6)     aperture-  = LATTICE(1)
 *   pressure+  = COLLAPSE(4)  pressure-  = VOID(0)
 *   depth+     = PROGRESS(3)  depth-     = RESET(9)
 *   binding+   = HARMONY(7)   binding-   = COUNTER(2)
 *   continuity+= BALANCE(5)   continuity-= BREATH(8)
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

module d2_clay (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        pipeline_clear,   // Clear history (new problem)

    // 5D force vector input (Q1.14 signed)
    input  wire signed [15:0] force_ap,  // aperture
    input  wire signed [15:0] force_pr,  // pressure
    input  wire signed [15:0] force_dp,  // depth
    input  wire signed [15:0] force_bn,  // binding
    input  wire signed [15:0] force_cn,  // continuity
    input  wire        force_valid,      // pulse to feed one vector

    // D2 output
    output reg  [3:0]  operator_out,     // classified operator 0-9
    output reg         operator_valid,   // pulse when ready
    output reg  [15:0] d2_magnitude      // |D2| of dominant dim (Q1.14)
);

    // =========================================================
    // History shift registers (3 taps, 5 dimensions each)
    // h0 = oldest, h1 = middle, h2 = newest
    // =========================================================
    reg signed [15:0] h0_ap, h0_pr, h0_dp, h0_bn, h0_cn;
    reg signed [15:0] h1_ap, h1_pr, h1_dp, h1_bn, h1_cn;
    reg signed [15:0] h2_ap, h2_pr, h2_dp, h2_bn, h2_cn;

    reg [1:0] fill;       // 0, 1, 2 = pipeline fill level
    reg       d2_valid;   // D2 computed this cycle

    // =========================================================
    // D2 results (18-bit signed for overflow safety)
    // =========================================================
    reg signed [17:0] d2_ap, d2_pr, d2_dp, d2_bn, d2_cn;

    // =========================================================
    // STAGE 1: Shift + D2 Compute
    // D2[dim] = h0[dim] - 2*h1[dim] + new[dim]
    // (uses pre-shift values: h0=oldest->h1, h1=middle->h2, new=newest)
    // =========================================================
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n || pipeline_clear) begin
            fill     <= 2'd0;
            d2_valid <= 1'b0;
            h0_ap <= 16'd0; h0_pr <= 16'd0; h0_dp <= 16'd0;
            h0_bn <= 16'd0; h0_cn <= 16'd0;
            h1_ap <= 16'd0; h1_pr <= 16'd0; h1_dp <= 16'd0;
            h1_bn <= 16'd0; h1_cn <= 16'd0;
            h2_ap <= 16'd0; h2_pr <= 16'd0; h2_dp <= 16'd0;
            h2_bn <= 16'd0; h2_cn <= 16'd0;
            d2_ap <= 18'd0; d2_pr <= 18'd0; d2_dp <= 18'd0;
            d2_bn <= 18'd0; d2_cn <= 18'd0;
        end else if (force_valid) begin
            // Shift history: h0 <- h1, h1 <- h2, h2 <- new
            h0_ap <= h1_ap; h0_pr <= h1_pr; h0_dp <= h1_dp;
            h0_bn <= h1_bn; h0_cn <= h1_cn;
            h1_ap <= h2_ap; h1_pr <= h2_pr; h1_dp <= h2_dp;
            h1_bn <= h2_bn; h1_cn <= h2_cn;
            h2_ap <= force_ap; h2_pr <= force_pr; h2_dp <= force_dp;
            h2_bn <= force_bn; h2_cn <= force_cn;

            // Track fill level
            if (fill < 2'd2)
                fill <= fill + 2'd1;

            // D2 = oldest - 2*middle + newest
            // At this point h1=old_oldest, h2=old_middle, force=new
            // After shift: new_h0=old_h1, new_h1=old_h2, new_h2=force
            // D2 uses pre-shift: oldest=h1, middle=h2, newest=force
            if (fill >= 2'd2) begin
                d2_ap <= {{2{h1_ap[15]}}, h1_ap}
                       - ({{2{h2_ap[15]}}, h2_ap} <<< 1)
                       + {{2{force_ap[15]}}, force_ap};
                d2_pr <= {{2{h1_pr[15]}}, h1_pr}
                       - ({{2{h2_pr[15]}}, h2_pr} <<< 1)
                       + {{2{force_pr[15]}}, force_pr};
                d2_dp <= {{2{h1_dp[15]}}, h1_dp}
                       - ({{2{h2_dp[15]}}, h2_dp} <<< 1)
                       + {{2{force_dp[15]}}, force_dp};
                d2_bn <= {{2{h1_bn[15]}}, h1_bn}
                       - ({{2{h2_bn[15]}}, h2_bn} <<< 1)
                       + {{2{force_bn[15]}}, force_bn};
                d2_cn <= {{2{h1_cn[15]}}, h1_cn}
                       - ({{2{h2_cn[15]}}, h2_cn} <<< 1)
                       + {{2{force_cn[15]}}, force_cn};
                d2_valid <= 1'b1;
            end else begin
                d2_valid <= 1'b0;
            end
        end else begin
            d2_valid <= 1'b0;
        end
    end

    // =========================================================
    // Absolute values (combinatorial from D2 regs)
    // =========================================================
    wire [17:0] abs_ap = d2_ap[17] ? (~d2_ap + 18'd1) : d2_ap;
    wire [17:0] abs_pr = d2_pr[17] ? (~d2_pr + 18'd1) : d2_pr;
    wire [17:0] abs_dp = d2_dp[17] ? (~d2_dp + 18'd1) : d2_dp;
    wire [17:0] abs_bn = d2_bn[17] ? (~d2_bn + 18'd1) : d2_bn;
    wire [17:0] abs_cn = d2_cn[17] ? (~d2_cn + 18'd1) : d2_cn;

    // =========================================================
    // STAGE 2: Classify (argmax |D2|, sign -> operator)
    // =========================================================
    reg [2:0]  max_dim_r;
    reg [17:0] max_val_r;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            operator_out   <= 4'd7;   // HARMONY default
            operator_valid <= 1'b0;
            d2_magnitude   <= 16'd0;
        end else if (d2_valid) begin
            // Find argmax of |D2| across 5 dimensions
            max_dim_r = 3'd0;
            max_val_r = abs_ap;
            if (abs_pr > max_val_r) begin max_dim_r = 3'd1; max_val_r = abs_pr; end
            if (abs_dp > max_val_r) begin max_dim_r = 3'd2; max_val_r = abs_dp; end
            if (abs_bn > max_val_r) begin max_dim_r = 3'd3; max_val_r = abs_bn; end
            if (abs_cn > max_val_r) begin max_dim_r = 3'd4; max_val_r = abs_cn; end

            // Map dimension + sign -> operator (0-9)
            case (max_dim_r)
                3'd0: operator_out <= d2_ap[17] ? 4'd1 : 4'd6;  // LATTICE / CHAOS
                3'd1: operator_out <= d2_pr[17] ? 4'd0 : 4'd4;  // VOID / COLLAPSE
                3'd2: operator_out <= d2_dp[17] ? 4'd9 : 4'd3;  // RESET / PROGRESS
                3'd3: operator_out <= d2_bn[17] ? 4'd2 : 4'd7;  // COUNTER / HARMONY
                3'd4: operator_out <= d2_cn[17] ? 4'd8 : 4'd5;  // BREATH / BALANCE
                default: operator_out <= 4'd0;
            endcase

            // Magnitude (truncate 18-bit to 16-bit, saturate)
            d2_magnitude   <= (max_val_r > 18'd65535) ? 16'hFFFF : max_val_r[15:0];
            operator_valid <= 1'b1;
        end else begin
            operator_valid <= 1'b0;
        end
    end

endmodule
