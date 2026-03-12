/*
 * ck_top_test.v -- AUTO-SWEEP DCLK FINDER
 *
 * Automatically cycles pixel clock through all 32 jm1 pins.
 * Each pin gets ~2 seconds. Full cycle = ~64 seconds.
 * All non-selected pins = HIGH (white data + DE/DISP).
 *
 * When LCD flashes white, read the current pin from LEDs:
 *   LED1 blinks FAST  (~6Hz) on the pin that works
 *   LED2 blinks SLOW  (~1.5Hz) always (alive)
 *
 * The sweep PAUSES for 4 seconds on any pin where it detects
 * it might be correct (actually it can't detect, so it just
 * cycles steadily). Watch for the LCD flash.
 *
 * Pin number encoding: The sweep goes 0,1,2,...,31,0,1,...
 * Each pin held for ~2 sec (cnt[25:0] rollover at 50MHz = 1.34s,
 * using cnt[26] for ~2.68s per pin).
 *
 * To identify the pin: when LCD lights up, the design also
 * outputs the 5-bit pin_sel on jm2[4:0] -- you can ignore this,
 * just count the position in the cycle. Cycle restarts roughly
 * every 86 seconds (32 × 2.68s).
 *
 * EASIER METHOD: The sweep also has a HOLD feature.
 * If LCD lights up, press KEY1 OR KEY2 (either button) to
 * FREEZE the sweep. Then count LED blinks:
 *   - After freezing, LED1 will blink N times then pause,
 *     where N = pin_sel (0-31). Repeats every ~4 seconds.
 *
 * Target: Puzhi PZ7020-StarLite (XC7Z020-2CLG400I)
 */

module ck_top_full (
    input  wire        pl_clk_50m,

    output wire        led1_n,
    output wire        led2_n,

    input  wire        key1_n,
    input  wire        key2_n,

    output wire        hdmi_clk_p,
    output wire        hdmi_clk_n,
    output wire [2:0]  hdmi_data_p,
    output wire [2:0]  hdmi_data_n,
    output wire        hdmi_out_en,
    input  wire        hdmi_hpd,
    output wire        hdmi_scl,
    inout  wire        hdmi_sda,

    output wire [31:0] jm1,
    output wire [31:0] jm2
);

    wire clk = pl_clk_50m;

    // =========================================================
    // HDMI: drive off via OBUFDS
    // =========================================================
    OBUFDS obuf_clk  (.I(1'b0), .O(hdmi_clk_p),    .OB(hdmi_clk_n));
    OBUFDS obuf_d0   (.I(1'b0), .O(hdmi_data_p[0]), .OB(hdmi_data_n[0]));
    OBUFDS obuf_d1   (.I(1'b0), .O(hdmi_data_p[1]), .OB(hdmi_data_n[1]));
    OBUFDS obuf_d2   (.I(1'b0), .O(hdmi_data_p[2]), .OB(hdmi_data_n[2]));
    assign hdmi_out_en = 1'b0;
    assign hdmi_scl    = 1'b1;

    // =========================================================
    // Main counter: 32-bit free-running
    // =========================================================
    reg [31:0] cnt;
    always @(posedge clk) begin
        cnt <= cnt + 32'd1;
    end

    // =========================================================
    // Pin selector: auto-sweep, bits [31:27] = pin_sel
    // Each pin held for cnt[26:0] rollover = 2^27 / 50MHz = ~2.68 sec
    // Full 32-pin cycle = ~86 seconds
    // =========================================================
    wire [4:0] pin_sel = cnt[31:27];

    // =========================================================
    // KEY debounce (either key freezes the sweep)
    // =========================================================
    reg [2:0] key1_sync, key2_sync;
    reg [19:0] key_deb;
    reg frozen;
    reg [4:0] frozen_pin;

    always @(posedge clk) begin
        key1_sync <= {key1_sync[1:0], key1_n};
        key2_sync <= {key2_sync[1:0], key2_n};
    end

    // Detect either key pressed (active-low)
    wire any_key_down = (~key1_sync[2]) | (~key2_sync[2]);

    always @(posedge clk) begin
        if (any_key_down && !frozen) begin
            if (key_deb == 20'hFFFFF) begin
                frozen <= 1'b1;
                frozen_pin <= pin_sel;
                key_deb <= 20'd0;
            end else begin
                key_deb <= key_deb + 20'd1;
            end
        end else if (!any_key_down) begin
            key_deb <= 20'd0;
        end
    end

    // Active pin: sweeping or frozen
    wire [4:0] active_pin = frozen ? frozen_pin : pin_sel;

    // =========================================================
    // LED display
    // =========================================================
    // LED2: always blink ~1.5 Hz (alive)
    assign led2_n = ~cnt[24];

    // LED1: In sweep mode, shows bit[0] of pin_sel (changes every ~2.7s)
    //        In frozen mode, blink out the pin number:
    //          Use a ~4 second cycle. Blink LED1 N times (N = frozen_pin+1)
    //          then stay off for remainder.

    reg led1_val;

    // Blink counter for frozen mode: 4-sec cycle = 2^28 / 50M ≈ 5.4 sec
    wire [7:0] blink_phase = cnt[27:20]; // 256 steps in ~5.4 sec
    // Each blink = 8 steps (on 4, off 4). Max 32 blinks = 256 steps.
    wire [4:0] blink_num = blink_phase[7:3]; // which blink (0-31)
    wire blink_on = ~blink_phase[2]; // on for first half of each blink slot

    always @(*) begin
        if (frozen) begin
            // Blink frozen_pin+1 times, then dark
            if (blink_num <= frozen_pin)
                led1_val = blink_on;
            else
                led1_val = 1'b0;
        end else begin
            // Sweep mode: toggle with pin changes
            led1_val = pin_sel[0] ^ cnt[22];
        end
    end

    assign led1_n = ~led1_val;

    // =========================================================
    // LCD pixel clock: 50 MHz / 6 ≈ 8.33 MHz
    // =========================================================
    reg [2:0] div;
    reg       pclk;
    always @(posedge clk) begin
        if (div == 3'd2) begin
            div  <= 3'd0;
            pclk <= ~pclk;
        end else begin
            div <= div + 3'd1;
        end
    end

    // =========================================================
    // DCLK SWEEP: selected pin gets pclk, all others HIGH
    // =========================================================
    genvar gi;
    generate
        for (gi = 0; gi < 32; gi = gi + 1) begin : pin_mux
            assign jm1[gi] = (active_pin == gi) ? pclk : 1'b1;
        end
    endgenerate

    // Output pin_sel on JM2 for debug (optional, read with scope)
    assign jm2[4:0]  = active_pin;
    assign jm2[31:5] = 27'd0;

endmodule
