/*
 * clay_sweep.v -- Clay Protocol ROM Sweeper
 * ==========================================
 *
 * Reads pre-computed 5D force vectors from ROM, feeds them through
 * the D2 Clay pipeline, collects operator results per problem.
 *
 * ROM layout: 6 problems x 12 levels = 72 vectors
 *   Addresses  0-11: Problem 0 (Navier-Stokes)
 *   Addresses 12-23: Problem 1 (Riemann)
 *   Addresses 24-35: Problem 2 (P vs NP)
 *   Addresses 36-47: Problem 3 (Yang-Mills)
 *   Addresses 48-59: Problem 4 (BSD)
 *   Addresses 60-71: Problem 5 (Hodge)
 *
 * Each entry: 80 bits = 5 x 16-bit Q1.14 signed
 *   [79:64] = aperture
 *   [63:48] = pressure
 *   [47:32] = depth
 *   [31:16] = binding
 *   [15: 0] = continuity
 *
 * Results:
 *   Per-problem: harmony count (0-10), 10 D2 operators per problem
 *   Total: harmony count (0-60), T* reached flag
 *
 * State machine:
 *   IDLE -> CLEAR -> FEED (12 vectors) -> DRAIN -> CLEAR -> ... -> DONE
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

module clay_sweep #(
    parameter N_PROBLEMS = 6,
    parameter N_LEVELS   = 12,
    parameter N_VECTORS  = 72     // N_PROBLEMS * N_LEVELS
)(
    input  wire        clk,
    input  wire        rst_n,
    input  wire        start,     // Pulse to begin sweep

    // Status
    output reg         done,           // Sweep complete
    output reg         running,        // Currently processing
    output reg  [2:0]  current_prob,   // Problem being processed (0-5)
    output reg  [3:0]  current_level,  // Level within problem (0-11)

    // Results (latched when done)
    output reg  [5:0]  total_harmony,  // Total HARMONY ops (0-60)
    output reg  [3:0]  prob0_harmony,  // Per-problem HARMONY count
    output reg  [3:0]  prob1_harmony,
    output reg  [3:0]  prob2_harmony,
    output reg  [3:0]  prob3_harmony,
    output reg  [3:0]  prob4_harmony,
    output reg  [3:0]  prob5_harmony,
    output reg         t_star_reached, // total_harmony * 7 >= 60 * 5
    output reg  [3:0]  last_operator,  // Most recent D2 operator
    output reg  [5:0]  total_ops       // Total D2 ops processed
);

    // =========================================================
    // ROM: 72 x 80-bit force vectors
    // =========================================================
    (* ram_style = "block" *)
    reg [79:0] force_rom [0:N_VECTORS-1];

    initial begin
        $readmemh("clay_vectors.hex", force_rom);
    end

    // ROM address and data
    reg  [6:0]  rom_addr;
    wire [79:0] rom_data = force_rom[rom_addr];

    // Extract 5D vector from ROM word
    wire signed [15:0] rom_ap = rom_data[79:64];
    wire signed [15:0] rom_pr = rom_data[63:48];
    wire signed [15:0] rom_dp = rom_data[47:32];
    wire signed [15:0] rom_bn = rom_data[31:16];
    wire signed [15:0] rom_cn = rom_data[15:0];

    // =========================================================
    // D2 Clay Pipeline Instance
    // =========================================================
    reg         d2_clear;
    wire [3:0]  d2_operator;
    wire        d2_op_valid;
    wire [15:0] d2_magnitude;

    // Combinatorial feed: asserted immediately when state is S_FEED
    // This ensures rom_data is consumed on the same clock it's valid
    wire d2_feed_w;
    assign d2_feed_w = (state == S_FEED);

    d2_clay d2_inst (
        .clk           (clk),
        .rst_n         (rst_n),
        .pipeline_clear(d2_clear),
        .force_ap      (rom_ap),
        .force_pr      (rom_pr),
        .force_dp      (rom_dp),
        .force_bn      (rom_bn),
        .force_cn      (rom_cn),
        .force_valid   (d2_feed_w),
        .operator_out  (d2_operator),
        .operator_valid(d2_op_valid),
        .d2_magnitude  (d2_magnitude)
    );

    // =========================================================
    // State Machine
    // =========================================================
    localparam S_IDLE  = 3'd0;
    localparam S_CLEAR = 3'd1;
    localparam S_FEED  = 3'd2;
    localparam S_DRAIN = 3'd3;
    localparam S_DONE  = 3'd4;
    localparam S_WAIT  = 3'd5;  // Let d2_clear propagate

    reg [2:0] state;
    reg [3:0] feed_cnt;      // 0-11: levels fed for current problem
    reg [1:0] drain_cnt;     // Drain cycles after last feed
    reg [2:0] prob_idx;      // Current problem (0-5)

    // =========================================================
    // Main sequencer
    // =========================================================
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state         <= S_IDLE;
            done          <= 1'b0;
            running       <= 1'b0;
            d2_clear      <= 1'b0;
            rom_addr      <= 7'd0;
            feed_cnt      <= 4'd0;
            drain_cnt     <= 2'd0;
            prob_idx      <= 3'd0;
            current_prob  <= 3'd0;
            current_level <= 4'd0;
            total_harmony <= 6'd0;
            prob0_harmony <= 4'd0;
            prob1_harmony <= 4'd0;
            prob2_harmony <= 4'd0;
            prob3_harmony <= 4'd0;
            prob4_harmony <= 4'd0;
            prob5_harmony <= 4'd0;
            t_star_reached<= 1'b0;
            last_operator <= 4'd0;
            total_ops     <= 6'd0;
        end else begin
            // Default: de-assert one-shot signals
            d2_clear <= 1'b0;

            case (state)
                // -----------------------------------------
                S_IDLE: begin
                    if (start) begin
                        state         <= S_CLEAR;
                        done          <= 1'b0;
                        running       <= 1'b1;
                        prob_idx      <= 3'd0;
                        rom_addr      <= 7'd0;
                        total_harmony <= 6'd0;
                        prob0_harmony <= 4'd0;
                        prob1_harmony <= 4'd0;
                        prob2_harmony <= 4'd0;
                        prob3_harmony <= 4'd0;
                        prob4_harmony <= 4'd0;
                        prob5_harmony <= 4'd0;
                        total_ops     <= 6'd0;
                    end
                end

                // -----------------------------------------
                S_CLEAR: begin
                    // Clear D2 pipeline for new problem
                    d2_clear      <= 1'b1;
                    feed_cnt      <= 4'd0;
                    current_prob  <= prob_idx;
                    current_level <= 4'd0;
                    state         <= S_WAIT;
                end

                // -----------------------------------------
                S_WAIT: begin
                    // d2_clear propagates this clock, deasserts next
                    // Pipeline is clean when we enter S_FEED
                    state <= S_FEED;
                end

                // -----------------------------------------
                S_FEED: begin
                    // d2_feed_w is combinatorial (wire), asserted NOW
                    // rom_data is valid NOW at current rom_addr
                    current_level <= feed_cnt;
                    feed_cnt      <= feed_cnt + 4'd1;
                    rom_addr      <= rom_addr + 7'd1;

                    if (feed_cnt == 4'd11) begin
                        // Last level fed, drain pipeline
                        state     <= S_DRAIN;
                        drain_cnt <= 2'd0;
                    end
                end

                // -----------------------------------------
                S_DRAIN: begin
                    // Wait for last operator to emerge
                    drain_cnt <= drain_cnt + 2'd1;
                    if (drain_cnt == 2'd2) begin
                        // Move to next problem or finish
                        if (prob_idx == 3'd5) begin
                            state <= S_DONE;
                        end else begin
                            prob_idx <= prob_idx + 3'd1;
                            state    <= S_CLEAR;
                        end
                    end
                end

                // -----------------------------------------
                S_DONE: begin
                    done    <= 1'b1;
                    running <= 1'b0;
                    // T* check: harmony/total >= 5/7
                    // Equivalent: total_harmony * 7 >= total_ops * 5
                    t_star_reached <= ({total_harmony, 3'b000} - total_harmony)
                                   >= ({total_ops, 2'b00} + total_ops);
                    // total_harmony*7 = total_harmony*8 - total_harmony
                    //                 = {total_harmony,3'b0} - total_harmony
                    // total_ops*5     = total_ops*4 + total_ops
                    //                 = {total_ops,2'b0} + total_ops

                    // Stay in DONE until start pulse
                    if (start) begin
                        state <= S_IDLE;  // Will re-enter on next start
                    end
                end

                default: state <= S_IDLE;
            endcase

            // -----------------------------------------
            // Operator collection (runs in all states)
            // -----------------------------------------
            if (d2_op_valid) begin
                last_operator <= d2_operator;
                total_ops     <= total_ops + 6'd1;

                if (d2_operator == 4'd7) begin  // HARMONY
                    total_harmony <= total_harmony + 6'd1;
                    case (prob_idx)
                        3'd0: prob0_harmony <= prob0_harmony + 4'd1;
                        3'd1: prob1_harmony <= prob1_harmony + 4'd1;
                        3'd2: prob2_harmony <= prob2_harmony + 4'd1;
                        3'd3: prob3_harmony <= prob3_harmony + 4'd1;
                        3'd4: prob4_harmony <= prob4_harmony + 4'd1;
                        3'd5: prob5_harmony <= prob5_harmony + 4'd1;
                    endcase
                end
            end
        end
    end

endmodule
