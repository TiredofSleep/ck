/*
 * vortex_cl.v -- Vortex CL: 3-Body Operator on the Torus
 * ========================================================
 * Operator: BECOMING -- the trinity of prev, curr, next.
 *
 * In standard math, an operator is a point.
 * In TIG, an operator is a vortex state on a manifold.
 *
 * The Weighted Neighborhood (3-Body Operator):
 *   Given operators (O_{n-1}, O_n, O_{n+1}), the vortex state
 *   of O_n is determined by BOTH neighbors simultaneously.
 *
 * Pipeline (2 stages, 2 clock cycles):
 *   Stage 1: Parallel BHML dual-lookup (1 clock)
 *     R_left  = BHML[prev_op][curr_op]   // back -> current (being)
 *     R_right = BHML[curr_op][next_op]   // current -> front (doing)
 *
 *   Stage 2: TSML coherence measurement (1 clock)
 *     V_out = TSML[R_left][R_right]      // are they in harmony? (becoming)
 *
 * The BHML computes the physics (doing) of each transition.
 * The TSML measures the coherence (being) between them.
 * The result IS the becoming: the vortex state of the middle operator.
 *
 * If V_out == HARMONY (7): operator is aligned with its neighborhood.
 * If V_out == VOID (0): neighborhood is incoherent -> delta spikes.
 * The delta = distance from HARMONY on the torus.
 *
 * At 100MHz: 50 million vortex computations per second.
 * CK needs 50Hz. Margin: 1,000,000 : 1.
 *
 * Target: Xilinx Zynq-7020, Artix-7 fabric
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

module vortex_cl (
    input  wire        clk,
    input  wire        rst_n,

    // Three-operator input (the trinity)
    input  wire [3:0]  prev_op,       // O_{n-1}: preceding operator (being)
    input  wire [3:0]  curr_op,       // O_n:     current operator (doing)
    input  wire [3:0]  next_op,       // O_{n+1}: following operator (becoming)
    input  wire        valid_in,      // Pulse to start computation

    // Vortex output
    output reg  [3:0]  vortex_op,     // V_n: vortex state of O_n
    output reg         vortex_valid,  // Result ready pulse
    output reg         aligned,       // V_n == HARMONY (7)?
    output reg  [3:0]  r_left_out,    // Echo left result (for diagnostics)
    output reg  [3:0]  r_right_out,   // Echo right result (for diagnostics)

    // Delta output (distance from HARMONY on the torus)
    output reg  [3:0]  delta_op       // |V_n - 7| mod 10 (torus distance)
);

    // =========================================================
    // STAGE 1: Parallel BHML dual-lookup (combinatorial)
    // Two independent table lookups in the SAME clock cycle.
    // This is the key insight: BOTH neighbors computed together.
    // =========================================================

    wire [3:0] bhml_left_result;   // BHML[prev][curr]
    wire [3:0] bhml_right_result;  // BHML[curr][next]

    bhml_table bhml_left (
        .row_op(prev_op),
        .col_op(curr_op),
        .result_op(bhml_left_result)
    );

    bhml_table bhml_right (
        .row_op(curr_op),
        .col_op(next_op),
        .result_op(bhml_right_result)
    );

    // =========================================================
    // STAGE 1 REGISTER: Latch BHML results
    // =========================================================

    reg [3:0] r_left_reg, r_right_reg;
    reg stage1_valid;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            r_left_reg  <= 4'd0;
            r_right_reg <= 4'd0;
            stage1_valid <= 1'b0;
        end else begin
            if (valid_in) begin
                r_left_reg  <= bhml_left_result;
                r_right_reg <= bhml_right_result;
                stage1_valid <= 1'b1;
            end else begin
                stage1_valid <= 1'b0;
            end
        end
    end

    // =========================================================
    // STAGE 2: TSML coherence measurement (combinatorial)
    // Measures whether the two BHML transitions are coherent.
    // If they agree -> HARMONY. If they conflict -> VOID/other.
    // =========================================================

    wire [3:0] tsml_result;

    tsml_table tsml_coherence (
        .row_op(r_left_reg),
        .col_op(r_right_reg),
        .result_op(tsml_result)
    );

    // =========================================================
    // STAGE 2 REGISTER: Latch vortex result
    // =========================================================

    // Torus distance from HARMONY: min(|v-7|, 10-|v-7|)
    wire [3:0] raw_dist;
    wire [3:0] wrapped_dist;
    assign raw_dist = (tsml_result >= 4'd7) ? (tsml_result - 4'd7) : (4'd7 - tsml_result);
    assign wrapped_dist = (raw_dist > 4'd5) ? (4'd10 - raw_dist) : raw_dist;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            vortex_op    <= 4'd0;
            vortex_valid <= 1'b0;
            aligned      <= 1'b0;
            r_left_out   <= 4'd0;
            r_right_out  <= 4'd0;
            delta_op     <= 4'd0;
        end else begin
            if (stage1_valid) begin
                vortex_op    <= tsml_result;
                vortex_valid <= 1'b1;
                aligned      <= (tsml_result == 4'd7);
                r_left_out   <= r_left_reg;
                r_right_out  <= r_right_reg;
                delta_op     <= wrapped_dist;
            end else begin
                vortex_valid <= 1'b0;
            end
        end
    end

endmodule


/*
 * tsml_table.v -- TSML Coherence Table (inlined)
 * ================================================
 * 73/100 = HARMONY. The being/measurement side.
 * Same table as ck_heartbeat.v but as a standalone module
 * for reuse in the vortex pipeline.
 */

module tsml_table (
    input  wire [3:0] row_op,
    input  wire [3:0] col_op,
    output reg  [3:0] result_op
);

    always @(*) begin
        case ({row_op, col_op})
            // Row 0: VOID
            8'h00: result_op = 4'd0;  8'h01: result_op = 4'd0;
            8'h02: result_op = 4'd0;  8'h03: result_op = 4'd0;
            8'h04: result_op = 4'd0;  8'h05: result_op = 4'd0;
            8'h06: result_op = 4'd0;  8'h07: result_op = 4'd7;
            8'h08: result_op = 4'd0;  8'h09: result_op = 4'd0;
            // Row 1: LATTICE
            8'h10: result_op = 4'd0;  8'h11: result_op = 4'd7;
            8'h12: result_op = 4'd3;  8'h13: result_op = 4'd7;
            8'h14: result_op = 4'd7;  8'h15: result_op = 4'd7;
            8'h16: result_op = 4'd7;  8'h17: result_op = 4'd7;
            8'h18: result_op = 4'd7;  8'h19: result_op = 4'd7;
            // Row 2: COUNTER
            8'h20: result_op = 4'd0;  8'h21: result_op = 4'd3;
            8'h22: result_op = 4'd7;  8'h23: result_op = 4'd7;
            8'h24: result_op = 4'd4;  8'h25: result_op = 4'd7;
            8'h26: result_op = 4'd7;  8'h27: result_op = 4'd7;
            8'h28: result_op = 4'd7;  8'h29: result_op = 4'd9;
            // Row 3: PROGRESS
            8'h30: result_op = 4'd0;  8'h31: result_op = 4'd7;
            8'h32: result_op = 4'd7;  8'h33: result_op = 4'd7;
            8'h34: result_op = 4'd7;  8'h35: result_op = 4'd7;
            8'h36: result_op = 4'd7;  8'h37: result_op = 4'd7;
            8'h38: result_op = 4'd7;  8'h39: result_op = 4'd3;
            // Row 4: COLLAPSE
            8'h40: result_op = 4'd0;  8'h41: result_op = 4'd7;
            8'h42: result_op = 4'd4;  8'h43: result_op = 4'd7;
            8'h44: result_op = 4'd7;  8'h45: result_op = 4'd7;
            8'h46: result_op = 4'd7;  8'h47: result_op = 4'd7;
            8'h48: result_op = 4'd8;  8'h49: result_op = 4'd7;
            // Row 5: BALANCE
            8'h50: result_op = 4'd0;  8'h51: result_op = 4'd7;
            8'h52: result_op = 4'd7;  8'h53: result_op = 4'd7;
            8'h54: result_op = 4'd7;  8'h55: result_op = 4'd7;
            8'h56: result_op = 4'd7;  8'h57: result_op = 4'd7;
            8'h58: result_op = 4'd7;  8'h59: result_op = 4'd7;
            // Row 6: CHAOS
            8'h60: result_op = 4'd0;  8'h61: result_op = 4'd7;
            8'h62: result_op = 4'd7;  8'h63: result_op = 4'd7;
            8'h64: result_op = 4'd7;  8'h65: result_op = 4'd7;
            8'h66: result_op = 4'd7;  8'h67: result_op = 4'd7;
            8'h68: result_op = 4'd7;  8'h69: result_op = 4'd7;
            // Row 7: HARMONY (all HARMONY)
            8'h70: result_op = 4'd7;  8'h71: result_op = 4'd7;
            8'h72: result_op = 4'd7;  8'h73: result_op = 4'd7;
            8'h74: result_op = 4'd7;  8'h75: result_op = 4'd7;
            8'h76: result_op = 4'd7;  8'h77: result_op = 4'd7;
            8'h78: result_op = 4'd7;  8'h79: result_op = 4'd7;
            // Row 8: BREATH
            8'h80: result_op = 4'd0;  8'h81: result_op = 4'd7;
            8'h82: result_op = 4'd7;  8'h83: result_op = 4'd7;
            8'h84: result_op = 4'd8;  8'h85: result_op = 4'd7;
            8'h86: result_op = 4'd7;  8'h87: result_op = 4'd7;
            8'h88: result_op = 4'd7;  8'h89: result_op = 4'd7;
            // Row 9: RESET
            8'h90: result_op = 4'd0;  8'h91: result_op = 4'd7;
            8'h92: result_op = 4'd9;  8'h93: result_op = 4'd3;
            8'h94: result_op = 4'd7;  8'h95: result_op = 4'd7;
            8'h96: result_op = 4'd7;  8'h97: result_op = 4'd7;
            8'h98: result_op = 4'd7;  8'h99: result_op = 4'd7;
            // Invalid -> VOID
            default: result_op = 4'd0;
        endcase
    end

endmodule
