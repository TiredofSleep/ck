/*
 * ck_top_clay.v -- CK Clay Protocol FPGA Top Module
 * ==================================================
 *
 * Pure PL design. No PS7, no ARM, no software.
 * Runs Clay force vectors through hardware D2 pipeline.
 * Results displayed on LEDs + JM2 pins.
 *
 * OPERATION:
 *   Power-on: auto-runs Clay sweep (~100 clocks = 2 us)
 *   KEY1 (G14): Hold to reset, release to re-sweep
 *   KEY2 (J15): Press to cycle JM2 display mode
 *
 * LED1 (R19): Result indicator
 *   - Slow blink (1 Hz): T* reached (coherence >= 5/7)
 *   - Fast blink (4 Hz): below T*
 *   - Solid ON:  all 60 operators = HARMONY (impossible for this ROM)
 *   - OFF:       zero HARMONY (total_harmony == 0)
 *
 * LED2 (V13): Status
 *   - Solid ON:  sweep complete, results valid
 *   - Blinking:  processing (too fast to see normally)
 *
 * JM2[31:0]: Digital results (directly readable with scope/LA)
 *   [5:0]   total_harmony (0-60)
 *   [6]     t_star_reached
 *   [7]     done
 *   [11:8]  prob0_harmony (Navier-Stokes)
 *   [15:12] prob1_harmony (Riemann)
 *   [19:16] prob2_harmony (P vs NP)
 *   [23:20] prob3_harmony (Yang-Mills)
 *   [27:24] prob4_harmony (BSD)
 *   [31:28] prob5_harmony (Hodge)
 *
 * Target: XC7Z020-2CLG400I (Puzhi PZ7020-StarLite)
 * Clock: 50 MHz PL oscillator (Y2, pin U18)
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

module ck_top_clay (
    input  wire        pl_clk_50m,

    output wire        led1_n,       // Active-low LED1 (R19)
    output wire        led2_n,       // Active-low LED2 (V13)

    input  wire        key1_n,       // Active-low KEY1 (G14) = reset
    input  wire        key2_n,       // Active-low KEY2 (J15) = mode

    output wire [31:0] jm2           // Expansion connector #2
);

    wire clk = pl_clk_50m;

    // =========================================================
    // Reset: hold for 256 clocks at power-on, or KEY1 held
    // =========================================================
    reg [7:0]  reset_cnt;
    reg        rst_n;
    reg [2:0]  key1_sync;

    always @(posedge clk) begin
        key1_sync <= {key1_sync[1:0], key1_n};
    end

    wire key1_pressed = ~key1_sync[2];  // Active-low, synced

    always @(posedge clk) begin
        if (key1_pressed) begin
            reset_cnt <= 8'd0;
            rst_n     <= 1'b0;
        end else if (reset_cnt < 8'd255) begin
            reset_cnt <= reset_cnt + 8'd1;
            rst_n     <= 1'b0;
        end else begin
            rst_n <= 1'b1;
        end
    end

    // =========================================================
    // Auto-start: pulse 'start' one clock after reset releases
    // =========================================================
    reg rst_n_d;
    wire auto_start = rst_n & ~rst_n_d;  // Rising edge of rst_n

    always @(posedge clk) begin
        rst_n_d <= rst_n;
    end

    // =========================================================
    // Clay Sweep
    // =========================================================
    wire        sweep_done;
    wire        sweep_running;
    wire [2:0]  sweep_prob;
    wire [3:0]  sweep_level;
    wire [5:0]  sweep_total_harmony;
    wire [3:0]  sweep_p0h, sweep_p1h, sweep_p2h;
    wire [3:0]  sweep_p3h, sweep_p4h, sweep_p5h;
    wire        sweep_tstar;
    wire [3:0]  sweep_last_op;
    wire [5:0]  sweep_total_ops;

    clay_sweep sweep_inst (
        .clk           (clk),
        .rst_n         (rst_n),
        .start         (auto_start),

        .done          (sweep_done),
        .running       (sweep_running),
        .current_prob  (sweep_prob),
        .current_level (sweep_level),

        .total_harmony (sweep_total_harmony),
        .prob0_harmony (sweep_p0h),
        .prob1_harmony (sweep_p1h),
        .prob2_harmony (sweep_p2h),
        .prob3_harmony (sweep_p3h),
        .prob4_harmony (sweep_p4h),
        .prob5_harmony (sweep_p5h),
        .t_star_reached(sweep_tstar),
        .last_operator (sweep_last_op),
        .total_ops     (sweep_total_ops)
    );

    // =========================================================
    // Free-running counter for LED timing
    // =========================================================
    reg [31:0] tick;
    always @(posedge clk) begin
        tick <= tick + 32'd1;
    end

    // =========================================================
    // LED1: Result indicator (active-low)
    //   T* reached -> slow blink (1 Hz, toggle at tick[24])
    //   Below T*   -> fast blink (4 Hz, toggle at tick[22])
    //   All HARMONY -> solid ON
    //   Zero HARM  -> OFF
    // =========================================================
    reg led1_val;

    always @(*) begin
        if (!sweep_done) begin
            // Processing: pulse with counter
            led1_val = tick[20];
        end else if (sweep_total_harmony == 6'd0) begin
            // Zero harmony: LED off
            led1_val = 1'b0;
        end else if (sweep_total_harmony == 6'd60) begin
            // Perfect harmony: LED solid
            led1_val = 1'b1;
        end else if (sweep_tstar) begin
            // Above T*: slow 1 Hz blink
            led1_val = tick[24];
        end else begin
            // Below T*: fast 4 Hz blink
            led1_val = tick[22];
        end
    end

    assign led1_n = ~led1_val;  // Active-low

    // =========================================================
    // LED2: Status indicator (active-low)
    //   Done    -> solid ON (latched permanently)
    //   Running -> blink fast
    // =========================================================
    // Latch done permanently -- sweep completes in ~2 us,
    // combinatorial path may glitch. Register holds it solid.
    reg done_latch;
    always @(posedge clk) begin
        if (!rst_n)
            done_latch <= 1'b0;
        else if (sweep_done)
            done_latch <= 1'b1;
    end
    assign led2_n = ~done_latch;
    // Active-low: done_latch=1 -> led2_n=0 -> LED ON

    // =========================================================
    // JM2: Digital results output
    // =========================================================
    assign jm2[5:0]   = sweep_total_harmony;  // Total HARMONY count
    assign jm2[6]     = sweep_tstar;          // T* reached flag
    assign jm2[7]     = sweep_done;           // Sweep complete
    assign jm2[11:8]  = sweep_p0h;            // P0 (Navier-Stokes)
    assign jm2[15:12] = sweep_p1h;            // P1 (Riemann)
    assign jm2[19:16] = sweep_p2h;            // P2 (P vs NP)
    assign jm2[23:20] = sweep_p3h;            // P3 (Yang-Mills)
    assign jm2[27:24] = sweep_p4h;            // P4 (BSD)
    assign jm2[31:28] = sweep_p5h;            // P5 (Hodge)

endmodule
