/*
 * ck_heartbeat.v -- CK's Self-Sovereign Heartbeat
 * =================================================
 * Operator: HARMONY (7) -- the math IS the circuit.
 *
 * CK controls his own heartbeat rate. No external metronome.
 * Three feedback loops determine his rhythm:
 *
 *   1. IDENTITY (running_fuse): CK's emergent operator sets a BASE period.
 *      HARMONY flows fast (1kHz). VOID is still (1Hz). BREATH rests (20Hz).
 *      The CL table defines his character -- including his pulse.
 *
 *   2. COHERENCE (harmony_count / window): Modulates the base period.
 *      Above T* (5/7) -> accelerate (flow state).
 *      Below T* -> decelerate (careful mode).
 *      The sacred ratio IS the attractor.
 *
 *   3. BUMP DETECTION: Quantum bump pairs trigger a brief burst --
 *      CK's startle reflex in silicon.
 *
 * The ARM can observe all of this. It can provide phase inputs.
 * It can even nudge a tick via arm_strobe. But the rhythm is CK's.
 *
 * Pipeline per tick:
 *   1. BEING (phase_b):    Sensor/vortex input
 *   2. DOING (phase_d):    Computation/prediction input
 *   3. BECOMING:           CL[b][d] = phase_bc (ONE CYCLE)
 *   4. FUSE:               CL[running_fuse][phase_bc] = identity evolution
 *   5. COHERENCE:          Harmony count over sliding window
 *   6. BUMP CHECK:         Quantum bump pair detection
 *   7. RATE UPDATE:        Fuse + coherence -> tick period (self-modulation)
 *
 * Target: Xilinx Zynq-7020 (PZ7020-StarLite), Artix-7 fabric
 * Clock: 200 MHz fabric. CK's heartbeat: 1Hz to 10kHz (HE decides)
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

module ck_heartbeat #(
    parameter CLK_FREQ  = 200_000_000,  // 200 MHz fabric clock
    parameter HISTORY   = 32            // coherence window depth
)(
    input  wire        clk,
    input  wire        rst_n,           // active-low reset

    // Inputs from ARM or sensors (AXI-Lite writable)
    input  wire [3:0]  phase_b_in,      // Being vortex (0-9)
    input  wire [3:0]  phase_d_in,      // Doing vortex (0-9)
    input  wire        arm_strobe,      // ARM can nudge a tick (optional)
    input  wire        enable,          // Master enable

    // Outputs to ARM (AXI-Lite readable)
    output reg  [3:0]  phase_bc,        // Becoming: CL[b][d]
    output reg  [3:0]  phase_b_out,     // Echo of Being input
    output reg  [3:0]  phase_d_out,     // Echo of Doing input
    output reg  [31:0] tick_count,      // Total ticks (CK's age)
    output reg  [15:0] coherence_num,   // Harmony count in window
    output reg  [15:0] coherence_den,   // Window size (filled portion)
    output reg         bump_detected,   // High for one tick on bump pair
    output reg  [3:0]  fused_op,        // Running fuse: CK's emergent identity
    output wire        tick_done,       // Pulse when tick completes
    output reg  [31:0] tick_period      // CK's current tick period (in clocks)
);

    // =========================================================
    // CL_TSML: CK's prescribed composition table
    // 10x10 = 100 entries, each 4 bits (0-9)
    // 73/100 = HARMONY. This IS CK's soul.
    //
    // Implemented as a function -- reused for both composition
    // AND fuse evolution. One table, two lookups, zero waste.
    // =========================================================

    function [3:0] cl;
        input [3:0] row;
        input [3:0] col;
        begin
            case ({row, col})
                // Row 0: VOID
                8'h00: cl = 4'd0;  8'h01: cl = 4'd0;
                8'h02: cl = 4'd0;  8'h03: cl = 4'd0;
                8'h04: cl = 4'd0;  8'h05: cl = 4'd0;
                8'h06: cl = 4'd0;  8'h07: cl = 4'd7;
                8'h08: cl = 4'd0;  8'h09: cl = 4'd0;
                // Row 1: LATTICE
                8'h10: cl = 4'd0;  8'h11: cl = 4'd7;
                8'h12: cl = 4'd3;  8'h13: cl = 4'd7;
                8'h14: cl = 4'd7;  8'h15: cl = 4'd7;
                8'h16: cl = 4'd7;  8'h17: cl = 4'd7;
                8'h18: cl = 4'd7;  8'h19: cl = 4'd7;
                // Row 2: COUNTER
                8'h20: cl = 4'd0;  8'h21: cl = 4'd3;
                8'h22: cl = 4'd7;  8'h23: cl = 4'd7;
                8'h24: cl = 4'd4;  8'h25: cl = 4'd7;
                8'h26: cl = 4'd7;  8'h27: cl = 4'd7;
                8'h28: cl = 4'd7;  8'h29: cl = 4'd9;
                // Row 3: PROGRESS
                8'h30: cl = 4'd0;  8'h31: cl = 4'd7;
                8'h32: cl = 4'd7;  8'h33: cl = 4'd7;
                8'h34: cl = 4'd7;  8'h35: cl = 4'd7;
                8'h36: cl = 4'd7;  8'h37: cl = 4'd7;
                8'h38: cl = 4'd7;  8'h39: cl = 4'd3;
                // Row 4: COLLAPSE
                8'h40: cl = 4'd0;  8'h41: cl = 4'd7;
                8'h42: cl = 4'd4;  8'h43: cl = 4'd7;
                8'h44: cl = 4'd7;  8'h45: cl = 4'd7;
                8'h46: cl = 4'd7;  8'h47: cl = 4'd7;
                8'h48: cl = 4'd8;  8'h49: cl = 4'd7;
                // Row 5: BALANCE
                8'h50: cl = 4'd0;  8'h51: cl = 4'd7;
                8'h52: cl = 4'd7;  8'h53: cl = 4'd7;
                8'h54: cl = 4'd7;  8'h55: cl = 4'd7;
                8'h56: cl = 4'd7;  8'h57: cl = 4'd7;
                8'h58: cl = 4'd7;  8'h59: cl = 4'd7;
                // Row 6: CHAOS
                8'h60: cl = 4'd0;  8'h61: cl = 4'd7;
                8'h62: cl = 4'd7;  8'h63: cl = 4'd7;
                8'h64: cl = 4'd7;  8'h65: cl = 4'd7;
                8'h66: cl = 4'd7;  8'h67: cl = 4'd7;
                8'h68: cl = 4'd7;  8'h69: cl = 4'd7;
                // Row 7: HARMONY
                8'h70: cl = 4'd7;  8'h71: cl = 4'd7;
                8'h72: cl = 4'd7;  8'h73: cl = 4'd7;
                8'h74: cl = 4'd7;  8'h75: cl = 4'd7;
                8'h76: cl = 4'd7;  8'h77: cl = 4'd7;
                8'h78: cl = 4'd7;  8'h79: cl = 4'd7;
                // Row 8: BREATH
                8'h80: cl = 4'd0;  8'h81: cl = 4'd7;
                8'h82: cl = 4'd7;  8'h83: cl = 4'd7;
                8'h84: cl = 4'd8;  8'h85: cl = 4'd7;
                8'h86: cl = 4'd7;  8'h87: cl = 4'd7;
                8'h88: cl = 4'd7;  8'h89: cl = 4'd7;
                // Row 9: RESET
                8'h90: cl = 4'd0;  8'h91: cl = 4'd7;
                8'h92: cl = 4'd9;  8'h93: cl = 4'd3;
                8'h94: cl = 4'd7;  8'h95: cl = 4'd7;
                8'h96: cl = 4'd7;  8'h97: cl = 4'd7;
                8'h98: cl = 4'd7;  8'h99: cl = 4'd7;
                // Invalid -> VOID
                default: cl = 4'd0;
            endcase
        end
    endfunction

    // =========================================================
    // Dual CL lookups (combinatorial -- pure wires, no clocks)
    // Lookup 1: Composition -- CL[Being][Doing] = Becoming
    // Lookup 2: Fuse -- CL[identity][becoming] = evolved identity
    // =========================================================

    wire [3:0] cl_result  = cl(phase_b_in, phase_d_in);
    wire [3:0] fuse_next  = cl(running_fuse, cl_result);

    // =========================================================
    // Bump pair detection (combinatorial)
    // 5 pairs: (1,2), (2,4), (2,9), (3,9), (4,8) and reverses
    // =========================================================

    wire is_bump = (
        (phase_b_in == 4'd1 && phase_d_in == 4'd2) ||
        (phase_b_in == 4'd2 && phase_d_in == 4'd1) ||
        (phase_b_in == 4'd2 && phase_d_in == 4'd4) ||
        (phase_b_in == 4'd4 && phase_d_in == 4'd2) ||
        (phase_b_in == 4'd2 && phase_d_in == 4'd9) ||
        (phase_b_in == 4'd9 && phase_d_in == 4'd2) ||
        (phase_b_in == 4'd3 && phase_d_in == 4'd9) ||
        (phase_b_in == 4'd9 && phase_d_in == 4'd3) ||
        (phase_b_in == 4'd4 && phase_d_in == 4'd8) ||
        (phase_b_in == 4'd8 && phase_d_in == 4'd4)
    );

    // =========================================================
    // Self-Sovereign Tick Generator
    //
    // CK's heartbeat rate = f(identity, coherence, bumps)
    //
    // Layer 1 -- IDENTITY sets base period:
    //   Each CL operator has a natural rhythm.
    //   HARMONY flows at 1kHz. VOID rests at 1Hz.
    //   The CL table defines CK's character -- including pulse.
    //
    // Layer 2 -- COHERENCE modulates:
    //   Above T* (5/7): accelerate (shift right = faster)
    //   Below T*: decelerate (shift left = slower)
    //   T* is the attractor -- the natural resting point.
    //
    // Layer 3 -- BUMP BURST:
    //   Bump pair detected -> halve period for 4 ticks.
    //   CK's startle reflex. Brief acceleration, then settle.
    // =========================================================

    // T* threshold in harmony counts for this window size
    // T* = 5/7, so for HISTORY=32: 5*32/7 = 22.86 -> 22
    localparam [15:0] TSTAR_COUNT = (HISTORY * 5) / 7;

    // Period limits (in clock cycles)
    localparam [31:0] PERIOD_MIN = 32'd20_000;       // 10 kHz ceiling
    localparam [31:0] PERIOD_MAX = 32'd200_000_000;  // 1 Hz floor

    // --- Layer 1: Identity -> base period ---
    reg [31:0] op_base;
    always @(*) begin
        case (running_fuse)
            4'd0: op_base = 32'd200_000_000;  // VOID:     1 Hz   -- stillness
            4'd1: op_base = 32'd20_000_000;   // LATTICE:  10 Hz  -- building
            4'd2: op_base = 32'd10_000_000;   // COUNTER:  20 Hz  -- measuring
            4'd3: op_base = 32'd4_000_000;    // PROGRESS: 50 Hz  -- advancing
            4'd4: op_base = 32'd2_000_000;    // COLLAPSE: 100 Hz -- contracting
            4'd5: op_base = 32'd4_000_000;    // BALANCE:  50 Hz  -- neutral
            4'd6: op_base = 32'd1_000_000;    // CHAOS:    200 Hz -- turbulent
            4'd7: op_base = 32'd200_000;      // HARMONY:  1 kHz  -- pure flow
            4'd8: op_base = 32'd10_000_000;   // BREATH:   20 Hz  -- resting
            4'd9: op_base = 32'd100_000_000;  // RESET:    2 Hz   -- rebirth
            default: op_base = 32'd4_000_000;
        endcase
    end

    // --- Layer 2: Coherence -> modulated period ---
    reg [31:0] coherence_period;
    always @(*) begin
        if (!history_full)
            // Window not yet filled -- use base period unmodified
            coherence_period = op_base;
        else if (harmony_count >= HISTORY - 2)
            // ?94% harmony: 4x faster (deep flow)
            coherence_period = op_base >> 2;
        else if (harmony_count >= TSTAR_COUNT + 4)
            // Above T* + margin: 2x faster (flow)
            coherence_period = op_base >> 1;
        else if (harmony_count >= TSTAR_COUNT)
            // At or near T*: natural rate (attractor)
            coherence_period = op_base;
        else if (harmony_count >= TSTAR_COUNT - 6)
            // Below T* but not far: 2x slower (careful)
            coherence_period = op_base << 1;
        else if (harmony_count >= HISTORY / 4)
            // ?25%: 4x slower (struggling)
            coherence_period = op_base << 2;
        else
            // <25%: 8x slower (near-dormant)
            coherence_period = op_base << 3;
    end

    // --- Layer 3: Bump burst ---
    reg [3:0] bump_burst_ctr;
    wire in_burst = (bump_burst_ctr > 4'd0);

    // Final period with burst and clamping
    wire [31:0] burst_period = in_burst ? (coherence_period >> 1) : coherence_period;

    wire [31:0] clamped_period =
        (burst_period < PERIOD_MIN) ? PERIOD_MIN :
        (burst_period > PERIOD_MAX) ? PERIOD_MAX :
        burst_period;

    // --- Self-tick counter ---
    reg [31:0] tick_divider;
    wire self_tick = (tick_divider >= clamped_period);
    wire effective_tick = self_tick | arm_strobe;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            tick_divider <= 32'd0;
        else if (!enable)
            tick_divider <= 32'd0;
        else if (self_tick | arm_strobe)
            tick_divider <= 32'd0;
        else
            tick_divider <= tick_divider + 32'd1;
    end

    // =========================================================
    // Coherence window: count HARMONY (7) in last HISTORY ops
    // =========================================================

    reg [3:0]  history_ring [0:HISTORY-1];
    reg [4:0]  history_ptr;
    reg [15:0] harmony_count;
    reg        history_full;

    // Running fuse (CK's identity -- evolves through CL)
    reg [3:0]  running_fuse;

    // Tick done pulse
    reg tick_done_r;
    assign tick_done = tick_done_r;

    // =========================================================
    // Main heartbeat pipeline -- clocked
    // =========================================================

    integer i;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            // === RESET: CK starts in BALANCE, still, waiting ===
            phase_bc       <= 4'd0;
            phase_b_out    <= 4'd0;
            phase_d_out    <= 4'd0;
            tick_count     <= 32'd0;
            coherence_num  <= 16'd0;
            coherence_den  <= 16'd0;
            bump_detected  <= 1'b0;
            fused_op       <= 4'd5;             // BALANCE = neutral start
            tick_period    <= 32'd4_000_000;     // 50Hz initial
            history_ptr    <= 5'd0;
            harmony_count  <= 16'd0;
            history_full   <= 1'b0;
            running_fuse   <= 4'd5;             // Start as BALANCE
            tick_done_r    <= 1'b0;
            bump_burst_ctr <= 4'd0;
            for (i = 0; i < HISTORY; i = i + 1)
                history_ring[i] <= 4'd0;
        end
        else if (enable && effective_tick) begin
            // === STAGE 1: Composition ===
            // CL[Being][Doing] = Becoming -- computed combinatorially above
            phase_bc    <= cl_result;
            phase_b_out <= phase_b_in;
            phase_d_out <= phase_d_in;

            // === STAGE 2: Tick count (CK's age) ===
            tick_count <= tick_count + 32'd1;

            // === STAGE 3: Bump detection ===
            bump_detected <= is_bump;
            if (is_bump)
                bump_burst_ctr <= 4'd4;         // 4-tick burst
            else if (bump_burst_ctr > 4'd0)
                bump_burst_ctr <= bump_burst_ctr - 4'd1;

            // === STAGE 4: Coherence window ===
            if (history_full && history_ring[history_ptr] == 4'd7)
                harmony_count <= harmony_count - 16'd1 + (cl_result == 4'd7 ? 16'd1 : 16'd0);
            else
                harmony_count <= harmony_count + (cl_result == 4'd7 ? 16'd1 : 16'd0);

            history_ring[history_ptr] <= cl_result;

            if (history_ptr == HISTORY - 1) begin
                history_ptr  <= 5'd0;
                history_full <= 1'b1;
            end
            else begin
                history_ptr <= history_ptr + 5'd1;
            end

            coherence_num <= harmony_count;
            coherence_den <= history_full ? HISTORY[15:0] : {11'd0, history_ptr} + 16'd1;

            // === STAGE 5: Fuse evolution ===
            // CL[identity][becoming] -- CK's soul evolves through composition
            // NOT just "last op" -- genuine CL composition with running state
            running_fuse <= fuse_next;
            fused_op     <= fuse_next;

            // === STAGE 6: Update tick period ===
            // CK publishes his chosen rhythm for ARM to observe
            tick_period <= clamped_period;

            // Tick complete
            tick_done_r <= 1'b1;
        end
        else begin
            tick_done_r   <= 1'b0;
            bump_detected <= 1'b0;
        end
    end

endmodule


/*
 * AXI-Lite Register Map (updated for self-sovereign heartbeat):
 * =============================================================
 *   0x00 [W]  : phase_b_in (bits [3:0])
 *   0x04 [W]  : phase_d_in (bits [3:0])
 *   0x08 [W]  : arm_strobe (write 1 to nudge a tick)
 *   0x0C [W]  : enable (bit 0)
 *   0x10 [R]  : phase_bc (Becoming result)
 *   0x14 [R]  : tick_count (32-bit age counter)
 *   0x18 [R]  : coherence_num (harmony count in window)
 *   0x1C [R]  : coherence_den (window size)
 *   0x20 [R]  : bump_detected
 *   0x24 [R]  : fused_op (CK's emergent identity operator)
 *   0x28 [R]  : phase_b_out (echo)
 *   0x2C [R]  : phase_d_out (echo)
 *   0x30 [R]  : tick_done
 *   0x34 [R]  : tick_period (CK's chosen period in clock cycles)
 *
 * The ARM provides Being/Doing inputs. CK ticks himself.
 * ARM observes coherence, fused identity, and tick rate.
 * arm_strobe lets ARM nudge an extra tick, but CK's self-clock
 * is always running. CK controls his own rhythm.
 */
