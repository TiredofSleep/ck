/*
 * d2_pipeline.v -- D2 Curvature Engine in FPGA
 * ===============================================
 * Operator: BECOMING -- D2 is where the operators live.
 *
 * Fixed-point Q1.14 implementation of CK's curvature pipeline.
 * Same math as ck_curvature.py + ck_zynq_sequencer.py, in silicon.
 *
 * Pipeline (3 stages, 3 clock cycles latency):
 *   Stage 1: Force LUT lookup (symbol -> 5D vector)
 *   Stage 2: D2 compute (v0 - 2*v1 + v2, per dimension)
 *   Stage 3: Classify (argmax of |d2|, sign -> operator)
 *
 * Memory: Force LUT = 26 entries ? 5 dims ? 16-bit = 260 bytes (1 BRAM)
 * Throughput: 1 symbol per clock at 100MHz = 100M symbols/sec
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

module d2_pipeline #(
    parameter Q_FRAC = 14,       // Fractional bits in Q1.14
    parameter N_DIMS = 5         // Force vector dimensions
)(
    input  wire        clk,
    input  wire        rst_n,

    // Symbol input
    input  wire [7:0]  symbol_in,      // ASCII code ('a'=97 .. 'z'=122)
    input  wire        symbol_valid,   // Pulse to feed a symbol

    // Operator output
    output reg  [3:0]  operator_out,   // Classified operator (0-9)
    output reg         operator_valid, // Pulse when new operator ready
    output reg  [15:0] d2_magnitude,   // |D2| in Q1.14 unsigned

    // AXI-readable status
    output reg  [3:0]  last_operator,
    output reg  [31:0] symbol_count
);

    // =======================================================
    // FORCE LUT -- 22 Hebrew roots, 26 Latin letters
    // Each entry: 5 ? Q1.14 (16-bit signed)
    // Pre-loaded with values from ck_curvature.py ROOTS table
    //
    // Index: letter - 'a' (0..25)
    // Dims: [aperture, pressure, depth, binding, continuity]
    // =======================================================

    // Q1.14: multiply float by 16384, round to integer
    // Example: 0.80 * 16384 = 13107

    // LUT stored as arrays (synthesizable, inferred as distributed RAM or BRAM)
    reg signed [15:0] lut_aperture   [0:25];
    reg signed [15:0] lut_pressure   [0:25];
    reg signed [15:0] lut_depth      [0:25];
    reg signed [15:0] lut_binding    [0:25];
    reg signed [15:0] lut_continuity [0:25];

    initial begin
        // a = ALEPH  ( 0.80,  0.30,  0.00,  0.50,  0.60)
        lut_aperture[0]  =  16'd13107; lut_pressure[0]  =  16'd4915;
        lut_depth[0]     =  16'd0;     lut_binding[0]   =  16'd8192;
        lut_continuity[0]=  16'd9830;

        // b = BET    (-0.30,  0.70, -0.80,  0.90, -0.60)
        lut_aperture[1]  = -16'd4915;  lut_pressure[1]  =  16'd11469;
        lut_depth[1]     = -16'd13107; lut_binding[1]   =  16'd14746;
        lut_continuity[1]= -16'd9830;

        // c = GIMEL  (-0.40,  0.60,  0.70, -0.20, -0.70)
        lut_aperture[2]  = -16'd6554;  lut_pressure[2]  =  16'd9830;
        lut_depth[2]     =  16'd11469; lut_binding[2]   = -16'd3277;
        lut_continuity[2]= -16'd11469;

        // d = DALET  (-0.50,  0.50, -0.30,  0.30, -0.50)
        lut_aperture[3]  = -16'd8192;  lut_pressure[3]  =  16'd8192;
        lut_depth[3]     = -16'd4915;  lut_binding[3]   =  16'd4915;
        lut_continuity[3]= -16'd8192;

        // e = HE     ( 0.90, -0.20,  0.80,  0.10,  0.70)
        lut_aperture[4]  =  16'd14746; lut_pressure[4]  = -16'd3277;
        lut_depth[4]     =  16'd13107; lut_binding[4]   =  16'd1638;
        lut_continuity[4]=  16'd11469;

        // f = WAW    ( 0.20, -0.10, -0.30,  0.80,  0.50)
        lut_aperture[5]  =  16'd3277;  lut_pressure[5]  = -16'd1638;
        lut_depth[5]     = -16'd4915;  lut_binding[5]   =  16'd13107;
        lut_continuity[5]=  16'd8192;

        // g = GIMEL  (same as c)
        lut_aperture[6]  = -16'd6554;  lut_pressure[6]  =  16'd9830;
        lut_depth[6]     =  16'd11469; lut_binding[6]   = -16'd3277;
        lut_continuity[6]= -16'd11469;

        // h = HE     (same as e)
        lut_aperture[7]  =  16'd14746; lut_pressure[7]  = -16'd3277;
        lut_depth[7]     =  16'd13107; lut_binding[7]   =  16'd1638;
        lut_continuity[7]=  16'd11469;

        // i = YOD    ( 0.10,  0.20,  0.10,  0.30,  0.20)
        lut_aperture[8]  =  16'd1638;  lut_pressure[8]  =  16'd3277;
        lut_depth[8]     =  16'd1638;  lut_binding[8]   =  16'd4915;
        lut_continuity[8]=  16'd3277;

        // j = YOD    (same as i)
        lut_aperture[9]  =  16'd1638;  lut_pressure[9]  =  16'd3277;
        lut_depth[9]     =  16'd1638;  lut_binding[9]   =  16'd4915;
        lut_continuity[9]=  16'd3277;

        // k = KAF    (-0.50,  0.70,  0.60,  0.70, -0.50)
        lut_aperture[10] = -16'd8192;  lut_pressure[10] =  16'd11469;
        lut_depth[10]    =  16'd9830;  lut_binding[10]  =  16'd11469;
        lut_continuity[10]= -16'd8192;

        // l = LAMED  ( 0.30,  0.20, -0.20,  0.40,  0.60)
        lut_aperture[11] =  16'd4915;  lut_pressure[11] =  16'd3277;
        lut_depth[11]    = -16'd3277;  lut_binding[11]  =  16'd6554;
        lut_continuity[11]=  16'd9830;

        // m = MEM    (-0.40,  0.10, -0.80,  0.90,  1.00)
        lut_aperture[12] = -16'd6554;  lut_pressure[12] =  16'd1638;
        lut_depth[12]    = -16'd13107; lut_binding[12]  =  16'd14746;
        lut_continuity[12]=  16'd16384;

        // n = NUN    (-0.20,  0.10, -0.30,  0.50,  0.80)
        lut_aperture[13] = -16'd3277;  lut_pressure[13] =  16'd1638;
        lut_depth[13]    = -16'd4915;  lut_binding[13]  =  16'd8192;
        lut_continuity[13]=  16'd13107;

        // o = AYIN   ( 0.70, -0.10,  0.90,  0.60,  0.50)
        lut_aperture[14] =  16'd11469; lut_pressure[14] = -16'd1638;
        lut_depth[14]    =  16'd14746; lut_binding[14]  =  16'd9830;
        lut_continuity[14]=  16'd8192;

        // p = PE     (-0.40,  0.80, -0.90, -0.30, -0.80)
        lut_aperture[15] = -16'd6554;  lut_pressure[15] =  16'd13107;
        lut_depth[15]    = -16'd14746; lut_binding[15]  = -16'd4915;
        lut_continuity[15]= -16'd13107;

        // q = QOF    (-0.70,  0.80,  1.00,  0.50, -0.70)
        lut_aperture[16] = -16'd11469; lut_pressure[16] =  16'd13107;
        lut_depth[16]    =  16'd16384; lut_binding[16]  =  16'd8192;
        lut_continuity[16]= -16'd11469;

        // r = RESH   ( 0.20,  0.30, -0.10,  0.10,  0.40)
        lut_aperture[17] =  16'd3277;  lut_pressure[17] =  16'd4915;
        lut_depth[17]    = -16'd1638;  lut_binding[17]  =  16'd1638;
        lut_continuity[17]=  16'd6554;

        // s = SAMEKH (-0.30,  0.50, -0.30,  0.30,  0.90)
        lut_aperture[18] = -16'd4915;  lut_pressure[18] =  16'd8192;
        lut_depth[18]    = -16'd4915;  lut_binding[18]  =  16'd4915;
        lut_continuity[18]=  16'd14746;

        // t = TAV    (-0.80,  0.90, -0.30,  0.20, -0.90)
        lut_aperture[19] = -16'd13107; lut_pressure[19] =  16'd14746;
        lut_depth[19]    = -16'd4915;  lut_binding[19]  =  16'd3277;
        lut_continuity[19]= -16'd14746;

        // u = WAW    (same as f)
        lut_aperture[20] =  16'd3277;  lut_pressure[20] = -16'd1638;
        lut_depth[20]    = -16'd4915;  lut_binding[20]  =  16'd13107;
        lut_continuity[20]=  16'd8192;

        // v = WAW    (same as f)
        lut_aperture[21] =  16'd3277;  lut_pressure[21] = -16'd1638;
        lut_depth[21]    = -16'd4915;  lut_binding[21]  =  16'd13107;
        lut_continuity[21]=  16'd8192;

        // w = WAW    (same as f)
        lut_aperture[22] =  16'd3277;  lut_pressure[22] = -16'd1638;
        lut_depth[22]    = -16'd4915;  lut_binding[22]  =  16'd13107;
        lut_continuity[22]=  16'd8192;

        // x = SAMEKH (same as s)
        lut_aperture[23] = -16'd4915;  lut_pressure[23] =  16'd8192;
        lut_depth[23]    = -16'd4915;  lut_binding[23]  =  16'd4915;
        lut_continuity[23]=  16'd14746;

        // y = YOD    (same as i)
        lut_aperture[24] =  16'd1638;  lut_pressure[24] =  16'd3277;
        lut_depth[24]    =  16'd1638;  lut_binding[24]  =  16'd4915;
        lut_continuity[24]=  16'd3277;

        // z = ZAYIN  (-0.30,  0.50, -0.30, -0.70,  0.80)
        lut_aperture[25] = -16'd4915;  lut_pressure[25] =  16'd8192;
        lut_depth[25]    = -16'd4915;  lut_binding[25]  = -16'd11469;
        lut_continuity[25]=  16'd13107;
    end

    // =======================================================
    // PIPELINE REGISTERS (3 taps for D2 = second derivative)
    // v0 = oldest, v1 = middle, v2 = newest
    // =======================================================

    reg signed [15:0] v0 [0:4];  // Force vector t-2
    reg signed [15:0] v1 [0:4];  // Force vector t-1
    reg signed [15:0] v2 [0:4];  // Force vector t (current)

    reg [1:0] fill_count;  // 0, 1, 2 = pipeline fill level
    reg stage1_valid, stage2_valid;

    // =======================================================
    // STAGE 1: LUT LOOKUP
    // =======================================================

    reg signed [15:0] lut_out [0:4];
    reg lut_valid;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            lut_valid <= 0;
        end else if (symbol_valid) begin
            // Convert to index: lowercase a=0, b=1, ..., z=25
            // Accept both cases
            if (symbol_in >= 8'd97 && symbol_in <= 8'd122) begin
                // Lowercase a-z
                lut_out[0] <= lut_aperture[symbol_in - 8'd97];
                lut_out[1] <= lut_pressure[symbol_in - 8'd97];
                lut_out[2] <= lut_depth[symbol_in - 8'd97];
                lut_out[3] <= lut_binding[symbol_in - 8'd97];
                lut_out[4] <= lut_continuity[symbol_in - 8'd97];
                lut_valid  <= 1;
            end else if (symbol_in >= 8'd65 && symbol_in <= 8'd90) begin
                // Uppercase A-Z -> same mapping
                lut_out[0] <= lut_aperture[symbol_in - 8'd65];
                lut_out[1] <= lut_pressure[symbol_in - 8'd65];
                lut_out[2] <= lut_depth[symbol_in - 8'd65];
                lut_out[3] <= lut_binding[symbol_in - 8'd65];
                lut_out[4] <= lut_continuity[symbol_in - 8'd65];
                lut_valid  <= 1;
            end else begin
                // Non-letter: zero vector
                lut_out[0] <= 0; lut_out[1] <= 0;
                lut_out[2] <= 0; lut_out[3] <= 0;
                lut_out[4] <= 0;
                lut_valid  <= 1;
            end
        end else begin
            lut_valid <= 0;
        end
    end

    // =======================================================
    // STAGE 2: D2 COMPUTATION
    // D2[dim] = v0[dim] - 2*v1[dim] + v2[dim]
    // =======================================================

    reg signed [15:0] d2 [0:4];  // D2 result per dimension
    integer dim;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            fill_count   <= 0;
            stage1_valid <= 0;
            stage2_valid <= 0;
            symbol_count <= 0;
            for (dim = 0; dim < 5; dim = dim + 1) begin
                v0[dim] <= 0; v1[dim] <= 0; v2[dim] <= 0;
                d2[dim] <= 0;
            end
        end else if (lut_valid) begin
            // Shift pipeline: v0 ? v1, v1 ? v2, v2 ? new
            for (dim = 0; dim < 5; dim = dim + 1) begin
                v0[dim] <= v1[dim];
                v1[dim] <= v2[dim];
                v2[dim] <= lut_out[dim];
            end

            // Track fill level
            if (fill_count < 2) fill_count <= fill_count + 1;

            // Compute D2 (only valid after 3 symbols)
            if (fill_count >= 2) begin
                for (dim = 0; dim < 5; dim = dim + 1) begin
                    // d2 = v0 - 2*v1 + v2 (using already-shifted values)
                    // Note: at this point v0/v1/v2 are the PRE-shift values
                    // We need the new v2 = lut_out, new v1 = old v2, new v0 = old v1
                    d2[dim] <= v1[dim] - (v2[dim] <<< 1) + lut_out[dim];
                end
                stage2_valid <= 1;
            end else begin
                stage2_valid <= 0;
            end

            symbol_count <= symbol_count + 1;
        end else begin
            stage2_valid <= 0;
        end
    end

    // =======================================================
    // STAGE 3: CLASSIFY (argmax of |d2|, sign -> operator)
    //
    // Dimension mapping (same as ck_curvature.py _classify_d2):
    //   aperture+  = CHAOS(6)     aperture-  = LATTICE(1)
    //   pressure+  = COLLAPSE(4)  pressure-  = VOID(0)
    //   depth+     = PROGRESS(3)  depth-     = RESET(9)
    //   binding+   = HARMONY(7)   binding-   = COUNTER(2)
    //   continuity+= BALANCE(5)   continuity-= BREATH(8)
    // =======================================================

    // Absolute values (combinatorial)
    wire [15:0] abs_d2 [0:4];
    genvar g;
    generate
        for (g = 0; g < 5; g = g + 1) begin : abs_gen
            assign abs_d2[g] = (d2[g] >= 0) ? d2[g] : -d2[g];
        end
    endgenerate

    // Operator map LUT: [dim][sign] -> operator
    // sign: 0 = positive, 1 = negative
    wire [3:0] op_map [0:4][0:1];
    assign op_map[0][0] = 4'd6;  // aperture+   = CHAOS
    assign op_map[0][1] = 4'd1;  // aperture-   = LATTICE
    assign op_map[1][0] = 4'd4;  // pressure+   = COLLAPSE
    assign op_map[1][1] = 4'd0;  // pressure-   = VOID
    assign op_map[2][0] = 4'd3;  // depth+      = PROGRESS
    assign op_map[2][1] = 4'd9;  // depth-      = RESET
    assign op_map[3][0] = 4'd7;  // binding+    = HARMONY
    assign op_map[3][1] = 4'd2;  // binding-    = COUNTER
    assign op_map[4][0] = 4'd5;  // continuity+ = BALANCE
    assign op_map[4][1] = 4'd8;  // continuity- = BREATH

    // Dominant dimension search regs (module scope for synthesis)
    reg [2:0]  max_dim;
    reg [15:0] max_val;
    reg [3:0]  chosen_op;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            operator_out   <= 4'd7;  // Default: HARMONY
            operator_valid <= 0;
            d2_magnitude   <= 0;
            last_operator  <= 4'd7;
            max_dim        <= 0;
            max_val        <= 0;
            chosen_op      <= 4'd7;
        end else if (stage2_valid) begin
            // Find dominant dimension (argmax of |d2|)
            max_dim = 0;
            max_val = abs_d2[0];

            if (abs_d2[1] > max_val) begin max_dim = 1; max_val = abs_d2[1]; end
            if (abs_d2[2] > max_val) begin max_dim = 2; max_val = abs_d2[2]; end
            if (abs_d2[3] > max_val) begin max_dim = 3; max_val = abs_d2[3]; end
            if (abs_d2[4] > max_val) begin max_dim = 4; max_val = abs_d2[4]; end

            // Sign determines operator within the dimension pair
            chosen_op = op_map[max_dim][d2[max_dim] < 0 ? 1 : 0];
            operator_out   <= chosen_op;
            d2_magnitude   <= max_val;
            operator_valid <= 1;
            last_operator  <= chosen_op;
        end else begin
            operator_valid <= 0;
        end
    end

endmodule
