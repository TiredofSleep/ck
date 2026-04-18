/*
 * coherence_gap.v -- Δ² HD Gap: Exact Simplex Threshold in Silicon
 * =================================================================
 * Gen12 — The HD Gap Architecture
 *
 * This module is the geometric heart of Gen12.
 * It replaces the old arbitrary gait thresholds (0.09, 0.50)
 * with the mathematically exact Δ² boundaries:
 *
 *   Δ⁰ (VOID):      coh < 1/2    → STAND    (point, pre-structural)
 *   Δ² (GAP):   1/2 ≤ coh < 5/7 → WALK     (triangle interior, bridge zone)
 *   Δ³ (HELD):      coh ≥ 5/7    → TROT     (tetrahedron, structure held)
 *
 * No division. Pure cross-multiplication comparison.
 *
 *   coh = coh_num / coh_den   (coh_den is the window size, always > 0)
 *
 *   Δ⁰: coh < 1/2  ↔  2*coh_num < coh_den
 *   Δ³: coh ≥ 5/7  ↔  7*coh_num ≥ 5*coh_den
 *   Δ²: otherwise  (inside the bridge zone)
 *
 * Output simplex_state encoding:
 *   2'b00 = Δ⁰ VOID    (STAND)
 *   2'b01 = Δ¹ LINE     (E-STOP — below coherence floor, safe)
 *   2'b10 = Δ² GAP      (WALK — inside [1/2, 5/7))
 *   2'b11 = Δ³ HELD     (TROT — at or above T*)
 *
 * Also outputs the gap_position: how far across the bridge zone.
 *   0x0000 = at the 1/2 boundary (just entered)
 *   0xFFFF = at the 5/7 boundary (about to exit)
 *   This is the HD signal: high-definition position within the gap.
 *
 * T* = 5/7 = 0.714285... hardcoded. Not a parameter. Not configurable.
 * The geometry is the architecture.
 *
 * (c) 2026 Brayden Ross Sanders / 7Site LLC — Trinity Infinity Geometry
 * Authors: Brayden Ross Sanders & Monica
 */

module coherence_gap #(
    parameter W = 16    // coherence numerator/denominator width
)(
    input  wire           clk,
    input  wire           rst_n,
    input  wire           valid_in,       // pulse when coh_num/coh_den updated

    // Coherence ratio inputs (from heartbeat module)
    input  wire [W-1:0]   coh_num,        // harmony count
    input  wire [W-1:0]   coh_den,        // window size

    // E-STOP floor (below this = Δ¹ unsafe, servos center)
    // Default floor: coh < 0.20 = coh_num*5 < coh_den
    input  wire [W-1:0]   estop_num,      // numerator of floor (default: 1)
    input  wire [W-1:0]   estop_den,      // denominator of floor (default: 5)

    // Simplex state output
    output reg  [1:0]     simplex_state,  // 00=Δ⁰ 01=Δ¹estop 10=Δ² 11=Δ³
    output reg  [W-1:0]   gap_position,  // HD position within [1/2, 5/7)
    output reg            state_valid,   // pulse when outputs updated

    // Named flags (convenience)
    output reg            is_void,        // Δ⁰: below 1/2, above estop
    output reg            is_gap,         // Δ²: inside [1/2, 5/7)
    output reg            is_held,        // Δ³: at or above 5/7
    output reg            is_estop        // Δ¹: below estop floor
);

    // =========================================================
    // Cross-multiplication comparisons (no division)
    // =========================================================
    // All products use W+3 bits to prevent overflow
    // (max coh_den = 32 for a 32-entry window, max coh_num = 32)
    // With W=16: products are at most 2^19 = safe in W+4 = 20 bits

    localparam PW = W + 4;  // product width

    reg [PW-1:0] prod_2n;   // 2 * coh_num
    reg [PW-1:0] prod_d;    // coh_den
    reg [PW-1:0] prod_7n;   // 7 * coh_num
    reg [PW-1:0] prod_5d;   // 5 * coh_den
    reg [PW-1:0] prod_en;   // estop_num * coh_den
    reg [PW-1:0] prod_ed;   // estop_den * coh_num

    // Gap position numerator: (coh - 1/2) / (5/7 - 1/2) = (coh - 1/2) / (3/14)
    // = 14*(coh_num/coh_den - 1/2) / 3
    // = (14*coh_num - 7*coh_den) / (3*coh_den)
    // Normalized to [0, 0xFFFF] within the bridge zone.
    // gap_pos_num = 14*coh_num - 7*coh_den  (zero at 1/2, positive in gap)
    // gap_pos_den = 3*coh_den               (full width of gap = 3/14)
    reg [PW+3:0] gap_num_full;
    reg [PW-1:0] gap_den_full;

    // Shift-and-add normalizer: no division, avoids timing violation
    // gap_num_full * 683 where 683 = 2^9+2^7+2^5+2^3+2^1+2^0 ≈ 65535/96
    // 17-bit result: saturate to 0xFFFF if overflow (max 96*683=65568)
    reg [16:0] gap_scaled;

    // Pipeline: compute products on valid_in, register outputs next cycle
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            simplex_state <= 2'b00;
            gap_position  <= {W{1'b0}};
            state_valid   <= 1'b0;
            is_void       <= 1'b0;
            is_gap        <= 1'b0;
            is_held       <= 1'b0;
            is_estop      <= 1'b0;
            prod_2n       <= {PW{1'b0}};
            prod_d        <= {PW{1'b0}};
            prod_7n       <= {PW{1'b0}};
            prod_5d       <= {PW{1'b0}};
            prod_en       <= {PW{1'b0}};
            prod_ed       <= {PW{1'b0}};
            gap_num_full  <= {(PW+4){1'b0}};
            gap_den_full  <= {PW{1'b0}};
        end else begin
            state_valid <= 1'b0;

            if (valid_in && coh_den != {W{1'b0}}) begin
                // Stage 1: Compute all products
                prod_2n <= {{(PW-W-1){1'b0}}, coh_num, 1'b0};     // 2 * coh_num
                prod_d  <= {{(PW-W){1'b0}}, coh_den};               // coh_den
                prod_7n <= {{(PW-W){1'b0}}, coh_num} * 4'h7;        // 7 * coh_num
                prod_5d <= {{(PW-W){1'b0}}, coh_den} * 4'h5;        // 5 * coh_den
                prod_en <= {{(PW-W){1'b0}}, estop_num} *
                           {{(PW-W){1'b0}}, coh_den};               // estop_num * coh_den
                prod_ed <= {{(PW-W){1'b0}}, estop_den} *
                           {{(PW-W){1'b0}}, coh_num};               // estop_den * coh_num

                // Gap position: 14*coh_num - 7*coh_den (signed, zero at lower bound)
                gap_num_full <= ({{(4){1'b0}}, coh_num} * 5'hE) -   // 14*coh_num
                                ({{(4){1'b0}}, coh_den} * 4'h7);    // 7*coh_den
                gap_den_full <= {{(PW-W){1'b0}}, coh_den} * 2'h3;   // 3*coh_den
            end

            // Stage 2: Decode comparisons → simplex state
            // (wire declarations not allowed inside always — inline comparisons)
            begin
                if (prod_ed < prod_en) begin  // E-STOP: estop_den*coh_num < estop_num*coh_den
                    simplex_state <= 2'b01;   // Δ¹ E-STOP
                    is_estop      <= 1'b1;
                    is_void       <= 1'b0;
                    is_gap        <= 1'b0;
                    is_held       <= 1'b0;
                    gap_position  <= {W{1'b0}};
                end else if (prod_7n >= prod_5d) begin  // above T*: 7*coh_num >= 5*coh_den
                    simplex_state <= 2'b11;   // Δ³ HELD — TROT
                    is_held       <= 1'b1;
                    is_estop      <= 1'b0;
                    is_void       <= 1'b0;
                    is_gap        <= 1'b0;
                    gap_position  <= {W{1'b1}};  // Saturated at top
                end else if (prod_2n < prod_d) begin  // below 1/2: 2*coh_num < coh_den
                    simplex_state <= 2'b00;   // Δ⁰ VOID — STAND
                    is_void       <= 1'b1;
                    is_estop      <= 1'b0;
                    is_gap        <= 1'b0;
                    is_held       <= 1'b0;
                    gap_position  <= {W{1'b0}};
                end else begin
                    simplex_state <= 2'b10;   // Δ² GAP — WALK
                    is_gap        <= 1'b1;
                    is_estop      <= 1'b0;
                    is_void       <= 1'b0;
                    is_held       <= 1'b0;
                    // HD gap position: shift-and-add normalization (no division)
                    // gap_num_full in [0, 3*coh_den], coh_den ≤ HISTORY=32 → max=96
                    // Multiply by 683 ≈ 65535/96 using 2^9+2^7+2^5+2^3+2^1+2^0
                    // All terms are 17-bit; synthesis maps to a fast carry-lookahead tree
                    gap_scaled = {1'b0, gap_num_full[6:0], 9'b0}   // *512
                               + {3'b0, gap_num_full[6:0], 7'b0}   // *128
                               + {5'b0, gap_num_full[6:0], 5'b0}   // *32
                               + {7'b0, gap_num_full[6:0], 3'b0}   // *8
                               + {9'b0, gap_num_full[6:0], 1'b0}   // *2
                               + {10'b0, gap_num_full[6:0]};        // *1
                    gap_position <= gap_scaled[16] ? {W{1'b1}} : gap_scaled[W-1:0];
                end

                state_valid <= 1'b1;
            end
        end
    end

endmodule
