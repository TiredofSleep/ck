/*
 * chain_walker.v -- Hardware Lattice Chain Walk Engine
 * =====================================================
 * Operator: LATTICE (1) -- the path IS the information.
 *
 * Implements CK's lattice chain walk in FPGA fabric.
 * Takes a stream of operators and walks them through
 * the BHML composition table pair-by-pair, building
 * a path through the CL algebra tree.
 *
 * Chain walk algorithm:
 *   1. Take operators in pairs: (O_0, O_1), (O_2, O_3), ...
 *   2. Compose each pair: R_k = BHML[O_{2k}][O_{2k+1}]
 *   3. The sequence of R_k IS the chain path
 *   4. Path depth = number of pair compositions
 *
 * Additionally computes vortex state at each step:
 *   V_k = TSML[R_{k-1}][R_k]
 *   This measures whether consecutive chain results are coherent.
 *
 * Path coherence = count(V_k == HARMONY) / depth
 * This is the chain-level equivalent of the heartbeat coherence window.
 *
 * Max chain depth: 16 (configurable)
 * Throughput: 1 pair per clock at 100MHz
 *
 * Target: Xilinx Zynq-7020, Artix-7 fabric
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

module chain_walker #(
    parameter MAX_DEPTH = 16,        // Maximum chain walk depth
    parameter DEPTH_BITS = 4         // log2(MAX_DEPTH)
)(
    input  wire        clk,
    input  wire        rst_n,

    // Operator input stream
    input  wire [3:0]  op_in,        // Operator to feed (0-9)
    input  wire        op_valid,     // Pulse to feed one operator
    input  wire        chain_start,  // Pulse to start a new chain walk
    input  wire        chain_end,    // Pulse to finalize results

    // Chain output
    output reg  [3:0]  path_op [0:MAX_DEPTH-1],  // Chain path results
    output reg  [DEPTH_BITS:0] path_depth,        // Current depth
    output reg  [3:0]  last_result,               // Most recent R_k
    output reg  [3:0]  last_vortex,               // Most recent V_k
    output reg         chain_done,                // Walk complete pulse

    // Coherence metrics
    output reg  [DEPTH_BITS:0] harmony_count,     // V_k == 7 count
    output reg  [15:0] coherence_num,             // harmony_count
    output reg  [15:0] coherence_den,             // path_depth
    output reg  [3:0]  dominant_op                // Most frequent path operator
);

    // =========================================================
    // State machine
    // =========================================================

    localparam S_IDLE    = 2'd0;
    localparam S_FIRST   = 2'd1;  // Waiting for first op of pair
    localparam S_SECOND  = 2'd2;  // Waiting for second op of pair
    localparam S_DONE    = 2'd3;

    reg [1:0] state;
    reg [3:0] first_op;          // First op of current pair
    reg [3:0] prev_result;       // Previous pair result (for vortex)
    reg       has_prev;          // Whether prev_result is valid

    // Operator histogram for dominant_op calculation
    reg [DEPTH_BITS:0] op_hist [0:9];

    // BHML lookup (combinatorial)
    wire [3:0] bhml_result;
    bhml_table bhml_chain (
        .row_op(first_op),
        .col_op(op_in),
        .result_op(bhml_result)
    );

    // TSML vortex lookup (combinatorial)
    wire [3:0] tsml_vortex;
    tsml_table tsml_chain (
        .row_op(prev_result),
        .col_op(bhml_result),
        .result_op(tsml_vortex)
    );

    integer i;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state         <= S_IDLE;
            path_depth    <= 0;
            last_result   <= 4'd0;
            last_vortex   <= 4'd0;
            chain_done    <= 1'b0;
            harmony_count <= 0;
            coherence_num <= 0;
            coherence_den <= 0;
            dominant_op   <= 4'd7;
            has_prev      <= 1'b0;
            first_op      <= 4'd0;
            prev_result   <= 4'd0;
            for (i = 0; i < MAX_DEPTH; i = i + 1)
                path_op[i] <= 4'd0;
            for (i = 0; i < 10; i = i + 1)
                op_hist[i] <= 0;
        end else begin
            chain_done <= 1'b0;

            case (state)
                S_IDLE: begin
                    if (chain_start) begin
                        // Reset for new walk
                        state         <= S_FIRST;
                        path_depth    <= 0;
                        harmony_count <= 0;
                        has_prev      <= 1'b0;
                        for (i = 0; i < MAX_DEPTH; i = i + 1)
                            path_op[i] <= 4'd0;
                        for (i = 0; i < 10; i = i + 1)
                            op_hist[i] <= 0;
                    end
                end

                S_FIRST: begin
                    if (chain_end) begin
                        // Finalize
                        state <= S_DONE;
                    end else if (op_valid) begin
                        // Store first op of pair
                        first_op <= op_in;
                        state    <= S_SECOND;
                    end
                end

                S_SECOND: begin
                    if (chain_end) begin
                        state <= S_DONE;
                    end else if (op_valid) begin
                        // COMPOSE: R_k = BHML[first_op][op_in]
                        // bhml_result is already computed combinatorially

                        if (path_depth < MAX_DEPTH) begin
                            // Store in path
                            path_op[path_depth] <= bhml_result;
                            last_result <= bhml_result;

                            // Update histogram
                            op_hist[bhml_result] <= op_hist[bhml_result] + 1;

                            // Vortex: V_k = TSML[R_{k-1}][R_k]
                            if (has_prev) begin
                                last_vortex <= tsml_vortex;
                                if (tsml_vortex == 4'd7)
                                    harmony_count <= harmony_count + 1;
                            end

                            // Update state
                            prev_result <= bhml_result;
                            has_prev    <= 1'b1;
                            path_depth  <= path_depth + 1;
                        end

                        state <= S_FIRST;  // Ready for next pair
                    end
                end

                S_DONE: begin
                    // Compute final metrics
                    coherence_num <= {11'd0, harmony_count};
                    coherence_den <= {11'd0, path_depth};

                    // Find dominant operator (simple max search)
                    // Unrolled for synthesis
                    begin
                        reg [3:0] best_op;
                        reg [DEPTH_BITS:0] best_count;
                        best_op = 4'd0;
                        best_count = op_hist[0];
                        if (op_hist[1] > best_count) begin best_op = 4'd1; best_count = op_hist[1]; end
                        if (op_hist[2] > best_count) begin best_op = 4'd2; best_count = op_hist[2]; end
                        if (op_hist[3] > best_count) begin best_op = 4'd3; best_count = op_hist[3]; end
                        if (op_hist[4] > best_count) begin best_op = 4'd4; best_count = op_hist[4]; end
                        if (op_hist[5] > best_count) begin best_op = 4'd5; best_count = op_hist[5]; end
                        if (op_hist[6] > best_count) begin best_op = 4'd6; best_count = op_hist[6]; end
                        if (op_hist[7] > best_count) begin best_op = 4'd7; best_count = op_hist[7]; end
                        if (op_hist[8] > best_count) begin best_op = 4'd8; best_count = op_hist[8]; end
                        if (op_hist[9] > best_count) begin best_op = 4'd9; best_count = op_hist[9]; end
                        dominant_op <= best_op;
                    end

                    chain_done <= 1'b1;
                    state      <= S_IDLE;
                end
            endcase
        end
    end

endmodule
