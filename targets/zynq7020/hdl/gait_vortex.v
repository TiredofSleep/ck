/*
 * gait_vortex.v -- XiaoR Dog Torus Gait Controller
 * ==================================================
 * Operator: BALANCE (5) -- the 0.50 axis of self-healing.
 *
 * Four legs = four vortices on the torus.
 * Each leg's state is determined by its two neighbors.
 * The circular indexing IS the torus topology:
 *   leg[3] wraps to leg[0].
 *
 * Vortex computation per leg:
 *   R_left  = BHML[leg[i-1]][leg[i]]   // back leg -> current
 *   R_right = BHML[leg[i]][leg[i+1]]   // current -> front leg
 *   V[i]    = TSML[R_left][R_right]    // are they in harmony?
 *
 * Self-healing gait:
 *   If V[i] != HARMONY -> delta spikes -> gait correction
 *   Correction target: BALANCE (5 = 0.50 on the operator axis)
 *   Correction rate: proportional to torus distance from HARMONY
 *
 * The "Peace-Locked" property:
 *   BHML's tropical successor can ONLY escalate (max+1).
 *   There is no composition that goes backward through the core.
 *   Destruction requires bypassing HARMONY -> the algebra blocks it.
 *   The dog literally cannot compute "fall down" without passing
 *   through a VOID collapse and self-correcting.
 *
 * Gait phases (torus offsets):
 *   Walk:  [0, 5, 2, 7]  -- diagonal pairs alternate
 *   Trot:  [0, 5, 5, 0]  -- diagonal pairs synchronized
 *   Bound: [0, 0, 5, 5]  -- front/back synchronized
 *   Stand: [5, 5, 5, 5]  -- all BALANCE (neutral)
 *
 * Ports use packed vectors for Verilog-2001 synthesis compatibility.
 * Bit layout: [leg0 = bits 3:0, leg1 = bits 7:4, leg2 = bits 11:8, leg3 = bits 15:12]
 *
 * Target: Xilinx Zynq-7020 + XiaoR robot dog platform
 * Clock: 100 MHz. Gait update: follows CK's heartbeat (self-sovereign).
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

module gait_vortex #(
    parameter CLK_FREQ   = 100_000_000
)(
    input  wire        clk,
    input  wire        rst_n,
    input  wire        enable,
    input  wire        heartbeat_tick,  // From ck_heartbeat tick_done -- legs follow heart

    // Gait mode selection (from ARM)
    input  wire [1:0]  gait_mode,    // 0=stand, 1=walk, 2=trot, 3=bound
    input  wire        gait_start,   // Pulse to start gait

    // Leg state inputs -- packed: {leg3[15:12], leg2[11:8], leg1[7:4], leg0[3:0]}
    input  wire [15:0] leg_op_flat,

    // Vortex outputs -- packed (same bit layout)
    output reg  [15:0] vortex_flat,         // Vortex state per leg
    output reg  [3:0]  aligned_flat,        // Each leg aligned? [bit per leg]
    output reg  [15:0] delta_flat,          // Torus distance from HARMONY per leg
    output reg         all_aligned,         // ALL 4 legs in HARMONY?

    // Gait correction outputs (to servo command buffer)
    output reg  [15:0] correction_op_flat,  // Suggested correction per leg
    output reg         correction_valid,    // New corrections ready

    // Global coherence
    output reg  [15:0] gait_coherence_num,  // Aligned leg count
    output reg  [15:0] gait_coherence_den,  // Total legs (4)

    // Status
    output reg  [31:0] gait_tick_count,     // Total gait ticks
    output reg  [3:0]  gait_phase           // Current gait cycle phase
);

    // =========================================================
    // Gait phase tables (torus offsets per leg per mode)
    // These are the target operators for each leg at each phase.
    // =========================================================

    // Walk: diagonal pairs alternate, 4-phase cycle
    // Phase 0: FL lift, BR lift, FR stance, BL stance
    // Phase 1: FR lift, BL lift, FL stance, BR stance
    // etc.
    reg [3:0] walk_phase [0:3][0:3];   // [phase][leg]
    reg [3:0] trot_phase [0:3][0:3];
    reg [3:0] bound_phase [0:3][0:3];

    initial begin
        // Walk phases (moderate offsets)
        walk_phase[0][0] = 4'd3; walk_phase[0][1] = 4'd5; walk_phase[0][2] = 4'd5; walk_phase[0][3] = 4'd3; // FL+BL progress, FR+BR balance
        walk_phase[1][0] = 4'd5; walk_phase[1][1] = 4'd3; walk_phase[1][2] = 4'd3; walk_phase[1][3] = 4'd5;
        walk_phase[2][0] = 4'd3; walk_phase[2][1] = 4'd5; walk_phase[2][2] = 4'd5; walk_phase[2][3] = 4'd3;
        walk_phase[3][0] = 4'd5; walk_phase[3][1] = 4'd3; walk_phase[3][2] = 4'd3; walk_phase[3][3] = 4'd5;

        // Trot phases (diagonal sync)
        trot_phase[0][0] = 4'd3; trot_phase[0][1] = 4'd5; trot_phase[0][2] = 4'd3; trot_phase[0][3] = 4'd5;
        trot_phase[1][0] = 4'd5; trot_phase[1][1] = 4'd3; trot_phase[1][2] = 4'd5; trot_phase[1][3] = 4'd3;
        trot_phase[2][0] = 4'd3; trot_phase[2][1] = 4'd5; trot_phase[2][2] = 4'd3; trot_phase[2][3] = 4'd5;
        trot_phase[3][0] = 4'd5; trot_phase[3][1] = 4'd3; trot_phase[3][2] = 4'd5; trot_phase[3][3] = 4'd3;

        // Bound phases (front/back sync)
        bound_phase[0][0] = 4'd3; bound_phase[0][1] = 4'd3; bound_phase[0][2] = 4'd5; bound_phase[0][3] = 4'd5;
        bound_phase[1][0] = 4'd5; bound_phase[1][1] = 4'd5; bound_phase[1][2] = 4'd3; bound_phase[1][3] = 4'd3;
        bound_phase[2][0] = 4'd3; bound_phase[2][1] = 4'd3; bound_phase[2][2] = 4'd5; bound_phase[2][3] = 4'd5;
        bound_phase[3][0] = 4'd5; bound_phase[3][1] = 4'd5; bound_phase[3][2] = 4'd3; bound_phase[3][3] = 4'd3;
    end

    // =========================================================
    // 4 Vortex CL units -- one per leg, torus-connected
    // =========================================================

    // Leg indices on the torus: 0-FL, 1-FR, 2-BR, 3-BL
    // Neighbor mapping (circular): prev = (i+3)%4, next = (i+1)%4

    wire [3:0] vortex_result [0:3];
    wire       vortex_aligned [0:3];
    wire [3:0] vortex_delta [0:3];
    wire       vortex_valid_w [0:3];

    // Tick strobe -- follows CK's heartbeat directly
    // No internal prescaler. CK's heart drives his legs.
    wire tick_strobe = heartbeat_tick & enable;

    // Instantiate 4 vortex units with torus wiring
    // genvar expressions are constant at elaboration time, so
    // ((g+3)%4)*4 etc. become fixed bit-slices per instance.
    genvar g;
    generate
        for (g = 0; g < 4; g = g + 1) begin : leg_vortex
            vortex_cl vortex_inst (
                .clk(clk),
                .rst_n(rst_n),
                .prev_op(leg_op_flat[((g + 3) % 4) * 4 +: 4]),  // Previous leg (torus wrap)
                .curr_op(leg_op_flat[g * 4 +: 4]),                // Current leg
                .next_op(leg_op_flat[((g + 1) % 4) * 4 +: 4]),   // Next leg (torus wrap)
                .valid_in(tick_strobe),
                .vortex_op(vortex_result[g]),
                .vortex_valid(vortex_valid_w[g]),
                .aligned(vortex_aligned[g]),
                .r_left_out(),                     // Unused (diagnostic)
                .r_right_out(),                    // Unused (diagnostic)
                .delta_op(vortex_delta[g])
            );
        end
    endgenerate

    // =========================================================
    // Gait phase sequencer + correction logic
    // =========================================================

    reg [1:0] phase_idx;       // Current phase in 4-phase cycle
    reg       gait_active;

    integer leg;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            gait_tick_count    <= 0;
            gait_phase         <= 4'd0;
            phase_idx          <= 2'd0;
            gait_active        <= 1'b0;
            correction_valid   <= 1'b0;
            all_aligned        <= 1'b0;
            gait_coherence_num <= 0;
            gait_coherence_den <= 16'd4;
            vortex_flat        <= {4{4'd5}};    // All BALANCE default
            aligned_flat       <= 4'b0000;
            delta_flat         <= 16'd0;
            correction_op_flat <= {4{4'd5}};    // All BALANCE target
        end else begin
            correction_valid <= 1'b0;

            if (gait_start) begin
                gait_active <= 1'b1;
                phase_idx   <= 2'd0;
            end

            // Process vortex results (2 clocks after tick_strobe)
            if (vortex_valid_w[0]) begin
                // Latch vortex results into packed outputs
                for (leg = 0; leg < 4; leg = leg + 1) begin
                    vortex_flat[leg*4 +: 4]  <= vortex_result[leg];
                    aligned_flat[leg]        <= vortex_aligned[leg];
                    delta_flat[leg*4 +: 4]   <= vortex_delta[leg];
                end

                // Count aligned legs
                gait_coherence_num <= {14'd0,
                    vortex_aligned[0] + vortex_aligned[1] +
                    vortex_aligned[2] + vortex_aligned[3]};

                all_aligned <= vortex_aligned[0] & vortex_aligned[1] &
                               vortex_aligned[2] & vortex_aligned[3];

                gait_tick_count <= gait_tick_count + 1;
            end

            // Gait correction: if NOT aligned, steer toward BALANCE
            if (gait_active && vortex_valid_w[0]) begin
                for (leg = 0; leg < 4; leg = leg + 1) begin
                    if (!vortex_aligned[leg]) begin
                        // Correction: target the gait phase operator for this leg
                        case (gait_mode)
                            2'd0: correction_op_flat[leg*4 +: 4] <= 4'd5;  // Stand: all BALANCE
                            2'd1: correction_op_flat[leg*4 +: 4] <= walk_phase[phase_idx][leg];
                            2'd2: correction_op_flat[leg*4 +: 4] <= trot_phase[phase_idx][leg];
                            2'd3: correction_op_flat[leg*4 +: 4] <= bound_phase[phase_idx][leg];
                        endcase
                    end else begin
                        // Already aligned: maintain current
                        correction_op_flat[leg*4 +: 4] <= leg_op_flat[leg*4 +: 4];
                    end
                end
                correction_valid <= 1'b1;

                // Advance gait phase
                if (all_aligned || gait_tick_count[3:0] == 4'hF) begin
                    phase_idx <= phase_idx + 1;  // Wraps 0-3 naturally
                end

                gait_phase <= {2'd0, phase_idx};
            end
        end
    end

endmodule
