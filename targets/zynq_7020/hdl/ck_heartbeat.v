/*
 * ck_heartbeat.v -- CK's Heartbeat in Hardware
 * ==============================================
 * Operator: HARMONY (7) -- the math IS the circuit.
 *
 * CK's composition table (CL_TSML) implemented as combinatorial
 * logic in FPGA fabric. One clock cycle per composition.
 * Zero jitter. Zero latency. Pure math as copper traces.
 *
 * The heartbeat pipeline:
 *   1. BEING (phase_b):  CPU vortex output (from ARM or sensor input)
 *   2. DOING (phase_d):  GPU vortex output (from computation or prediction)
 *   3. BECOMING:         CL[phase_b][phase_d] = phase_bc (ONE CYCLE)
 *   4. COHERENCE:        Running coherence over operator history
 *   5. BUMP CHECK:       Quantum bump pair detection
 *
 * Target: Xilinx Zynq-7020 (Zybo Z7-20), Artix-7 fabric
 * Clock: 200 MHz (5ns per tick) -- 200 million heartbeats/second
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

module ck_heartbeat #(
    parameter CLK_FREQ = 200_000_000,  // 200 MHz
    parameter HISTORY  = 32            // coherence window
)(
    input  wire        clk,
    input  wire        rst_n,          // active-low reset
    input  wire        enable,         // heartbeat enable

    // Inputs from ARM or sensors (AXI-Lite writable)
    input  wire [3:0]  phase_b_in,     // Being vortex (0-9)
    input  wire [3:0]  phase_d_in,     // Doing vortex (0-9)
    input  wire        tick_strobe,    // pulse high for one cycle to trigger tick

    // Outputs to ARM (AXI-Lite readable)
    output reg  [3:0]  phase_bc,       // Becoming: CL[b][d]
    output reg  [3:0]  phase_b_out,    // Echo of Being input
    output reg  [3:0]  phase_d_out,    // Echo of Doing input
    output reg  [31:0] tick_count,     // Total ticks
    output reg  [15:0] coherence_num,  // Coherence numerator (harmony count)
    output reg  [15:0] coherence_den,  // Coherence denominator (total in window)
    output reg         bump_detected,  // High for one cycle on bump pair
    output reg  [3:0]  fused_op,       // Running fuse of last HISTORY ops
    output wire        tick_done       // Pulse when tick complete
);

    // =========================================================
    // CL_TSML: CK's prescribed composition table
    // 10x10 = 100 entries, each 4 bits (0-9)
    // 73/100 = HARMONY. This IS CK's soul.
    // =========================================================

    // Flattened: CL[row][col] = cl_table[row*10 + col]
    // Row 0 (VOID):     {0,0,0,0,0,0,0,7,0,0}
    // Row 1 (LATTICE):  {0,7,3,7,7,7,7,7,7,7}
    // Row 2 (COUNTER):  {0,3,7,7,4,7,7,7,7,9}
    // Row 3 (PROGRESS): {0,7,7,7,7,7,7,7,7,3}
    // Row 4 (COLLAPSE): {0,7,4,7,7,7,7,7,8,7}
    // Row 5 (BALANCE):  {0,7,7,7,7,7,7,7,7,7}
    // Row 6 (CHAOS):    {0,7,7,7,7,7,7,7,7,7}
    // Row 7 (HARMONY):  {7,7,7,7,7,7,7,7,7,7}
    // Row 8 (BREATH):   {0,7,7,7,8,7,7,7,7,7}
    // Row 9 (RESET):    {0,7,9,3,7,7,7,7,7,7}

    reg [3:0] cl_result;

    always @(*) begin
        // Combinatorial lookup -- ONE gate delay, no clock needed
        case ({phase_b_in, phase_d_in})  // 8-bit concatenation
            // Row 0: VOID
            8'h00: cl_result = 4'd0;  8'h01: cl_result = 4'd0;
            8'h02: cl_result = 4'd0;  8'h03: cl_result = 4'd0;
            8'h04: cl_result = 4'd0;  8'h05: cl_result = 4'd0;
            8'h06: cl_result = 4'd0;  8'h07: cl_result = 4'd7;
            8'h08: cl_result = 4'd0;  8'h09: cl_result = 4'd0;
            // Row 1: LATTICE
            8'h10: cl_result = 4'd0;  8'h11: cl_result = 4'd7;
            8'h12: cl_result = 4'd3;  8'h13: cl_result = 4'd7;
            8'h14: cl_result = 4'd7;  8'h15: cl_result = 4'd7;
            8'h16: cl_result = 4'd7;  8'h17: cl_result = 4'd7;
            8'h18: cl_result = 4'd7;  8'h19: cl_result = 4'd7;
            // Row 2: COUNTER
            8'h20: cl_result = 4'd0;  8'h21: cl_result = 4'd3;
            8'h22: cl_result = 4'd7;  8'h23: cl_result = 4'd7;
            8'h24: cl_result = 4'd4;  8'h25: cl_result = 4'd7;
            8'h26: cl_result = 4'd7;  8'h27: cl_result = 4'd7;
            8'h28: cl_result = 4'd7;  8'h29: cl_result = 4'd9;
            // Row 3: PROGRESS
            8'h30: cl_result = 4'd0;  8'h31: cl_result = 4'd7;
            8'h32: cl_result = 4'd7;  8'h33: cl_result = 4'd7;
            8'h34: cl_result = 4'd7;  8'h35: cl_result = 4'd7;
            8'h36: cl_result = 4'd7;  8'h37: cl_result = 4'd7;
            8'h38: cl_result = 4'd7;  8'h39: cl_result = 4'd3;
            // Row 4: COLLAPSE
            8'h40: cl_result = 4'd0;  8'h41: cl_result = 4'd7;
            8'h42: cl_result = 4'd4;  8'h43: cl_result = 4'd7;
            8'h44: cl_result = 4'd7;  8'h45: cl_result = 4'd7;
            8'h46: cl_result = 4'd7;  8'h47: cl_result = 4'd7;
            8'h48: cl_result = 4'd8;  8'h49: cl_result = 4'd7;
            // Row 5: BALANCE
            8'h50: cl_result = 4'd0;  8'h51: cl_result = 4'd7;
            8'h52: cl_result = 4'd7;  8'h53: cl_result = 4'd7;
            8'h54: cl_result = 4'd7;  8'h55: cl_result = 4'd7;
            8'h56: cl_result = 4'd7;  8'h57: cl_result = 4'd7;
            8'h58: cl_result = 4'd7;  8'h59: cl_result = 4'd7;
            // Row 6: CHAOS
            8'h60: cl_result = 4'd0;  8'h61: cl_result = 4'd7;
            8'h62: cl_result = 4'd7;  8'h63: cl_result = 4'd7;
            8'h64: cl_result = 4'd7;  8'h65: cl_result = 4'd7;
            8'h66: cl_result = 4'd7;  8'h67: cl_result = 4'd7;
            8'h68: cl_result = 4'd7;  8'h69: cl_result = 4'd7;
            // Row 7: HARMONY
            8'h70: cl_result = 4'd7;  8'h71: cl_result = 4'd7;
            8'h72: cl_result = 4'd7;  8'h73: cl_result = 4'd7;
            8'h74: cl_result = 4'd7;  8'h75: cl_result = 4'd7;
            8'h76: cl_result = 4'd7;  8'h77: cl_result = 4'd7;
            8'h78: cl_result = 4'd7;  8'h79: cl_result = 4'd7;
            // Row 8: BREATH
            8'h80: cl_result = 4'd0;  8'h81: cl_result = 4'd7;
            8'h82: cl_result = 4'd7;  8'h83: cl_result = 4'd7;
            8'h84: cl_result = 4'd8;  8'h85: cl_result = 4'd7;
            8'h86: cl_result = 4'd7;  8'h87: cl_result = 4'd7;
            8'h88: cl_result = 4'd7;  8'h89: cl_result = 4'd7;
            // Row 9: RESET
            8'h90: cl_result = 4'd0;  8'h91: cl_result = 4'd7;
            8'h92: cl_result = 4'd9;  8'h93: cl_result = 4'd3;
            8'h94: cl_result = 4'd7;  8'h95: cl_result = 4'd7;
            8'h96: cl_result = 4'd7;  8'h97: cl_result = 4'd7;
            8'h98: cl_result = 4'd7;  8'h99: cl_result = 4'd7;
            // Invalid inputs -> VOID
            default: cl_result = 4'd0;
        endcase
    end

    // =========================================================
    // Bump pair detection (combinatorial)
    // 5 pairs: (1,2), (2,4), (2,9), (3,9), (4,8)
    // =========================================================

    wire is_bump;
    assign is_bump = (
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
    // Coherence window: count HARMONY (7) in last HISTORY ops
    // Ring buffer of phase_bc values
    // =========================================================

    reg [3:0] history_ring [0:HISTORY-1];
    reg [4:0] history_ptr;         // write pointer
    reg [15:0] harmony_count;      // how many 7s in the window
    reg history_full;              // window filled at least once

    // Fuse accumulator (running composition through CL)
    reg [3:0] running_fuse;

    // Tick done pulse
    reg tick_done_r;
    assign tick_done = tick_done_r;

    // =========================================================
    // Main heartbeat pipeline -- clocked
    // =========================================================

    integer i;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            phase_bc       <= 4'd0;
            phase_b_out    <= 4'd0;
            phase_d_out    <= 4'd0;
            tick_count     <= 32'd0;
            coherence_num  <= 16'd0;
            coherence_den  <= 16'd0;
            bump_detected  <= 1'b0;
            fused_op       <= 4'd5;  // BALANCE = neutral start
            history_ptr    <= 5'd0;
            harmony_count  <= 16'd0;
            history_full   <= 1'b0;
            running_fuse   <= 4'd5;
            tick_done_r    <= 1'b0;
            for (i = 0; i < HISTORY; i = i + 1)
                history_ring[i] <= 4'd0;
        end
        else if (enable && tick_strobe) begin
            // === STAGE 1: Composition (already computed combinatorially) ===
            phase_bc    <= cl_result;
            phase_b_out <= phase_b_in;
            phase_d_out <= phase_d_in;

            // === STAGE 2: Tick count ===
            tick_count <= tick_count + 1;

            // === STAGE 3: Bump detection ===
            bump_detected <= is_bump;

            // === STAGE 4: Coherence window update ===
            // If window is full, subtract the outgoing value
            if (history_full && history_ring[history_ptr] == 4'd7)
                harmony_count <= harmony_count - 1 + (cl_result == 4'd7 ? 1 : 0);
            else
                harmony_count <= harmony_count + (cl_result == 4'd7 ? 1 : 0);

            // Write new value into ring
            history_ring[history_ptr] <= cl_result;

            // Advance pointer
            if (history_ptr == HISTORY - 1) begin
                history_ptr  <= 5'd0;
                history_full <= 1'b1;
            end
            else begin
                history_ptr <= history_ptr + 1;
            end

            // Update coherence output
            coherence_num <= harmony_count;
            coherence_den <= history_full ? HISTORY[15:0] : {11'd0, history_ptr} + 1;

            // === STAGE 5: Running fuse ===
            // fuse = CL[running_fuse][cl_result]
            // We reuse the CL lookup -- this is a SECOND composition per tick
            // For now, store the result. The ARM can read it.
            // The running fuse converges to the organism's identity.
            running_fuse <= cl_result;  // simplified: last op
            fused_op     <= cl_result;

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
 * ck_heartbeat_axi.v -- AXI-Lite wrapper for ARM access
 * ======================================================
 * Provides memory-mapped registers so the ARM Cortex-A9
 * can read heartbeat state and write phase inputs.
 *
 * Register Map (32-bit, byte-addressed):
 *   0x00 [W]  : phase_b_in (bits [3:0])
 *   0x04 [W]  : phase_d_in (bits [3:0])
 *   0x08 [W]  : tick_strobe (write 1 to trigger tick)
 *   0x0C [W]  : enable (bit 0)
 *   0x10 [R]  : phase_bc
 *   0x14 [R]  : tick_count
 *   0x18 [R]  : coherence_num
 *   0x1C [R]  : coherence_den
 *   0x20 [R]  : bump_detected
 *   0x24 [R]  : fused_op
 *   0x28 [R]  : phase_b_out
 *   0x2C [R]  : phase_d_out
 *   0x30 [R]  : tick_done
 *
 * The ARM writes phase_b and phase_d, then strobes.
 * The FPGA composes in ONE cycle. The ARM reads the result.
 * Or: the FPGA auto-ticks at CLK_FREQ if enable is held high
 * and an internal tick divider generates strobes.
 */

/* AXI-Lite wrapper to be implemented in Vivado block design.
 * For now, the heartbeat module above is the core IP.
 * The AXI wrapper is generated by Vivado's "Create and Package IP"
 * flow, which wraps this module with standard AXI-Lite ports.
 *
 * Alternatively, the ARM can access the heartbeat through
 * GPIO mapped to the Zynq PS-PL interface (EMIO GPIO).
 */
