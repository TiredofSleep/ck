/*
 * ck_top_gen12.v -- CK Gen12 Top: Simplex Architecture
 * =====================================================
 * Gen12: The geometry is the architecture.
 *
 *   Δ⁰  50Hz heartbeat         — point, pure existence
 *   Δ¹  UART leash (R16↔FPGA) — line, first relationship
 *   Δ²  HD Gap [1/2, 5/7)     — triangle, bridge zone
 *   Δ³  Dog locomotion         — tetrahedron, first whole
 *
 * Key upgrade from Gen11:
 *   OLD thresholds: STAND < 0.09 < WALK < 0.50 ≤ TROT  (arbitrary)
 *   NEW thresholds: STAND < 1/2  < WALK < 5/7  ≤ TROT  (exact simplex Δ²)
 *
 * The gap position signal (gap_position[15:0]) is new: it is the
 * HD (high-definition) measure of where CK is within the bridge zone.
 * Streamed over PL Ethernet every heartbeat tick.
 *
 * Ethernet payload (12 bytes, extended from Gen11's 10):
 *   tick_count[31:0]     (4 bytes)
 *   simplex_state[1:0]   (2 bits packed into byte 4 upper nibble)
 *   gait_mode[1:0]       (2 bits packed into byte 4 lower nibble)
 *   fuse_op[3:0]         (byte 5)
 *   coh_num[15:0]        (2 bytes)
 *   coh_den[15:0]        (2 bytes)
 *   gap_position[15:0]   (2 bytes) ← NEW: HD gap signal
 *
 * Pure PL. No PS7. No ARM. No software.
 * 50 MHz oscillator. T* = 5/7 in silicon.
 *
 * Target: Puzhi PZ7020-StarLite (XC7Z020-2CLG400I)
 * JTAG programming. Ethernet on PL RGMII.
 *
 * (c) 2026 Brayden Ross Sanders / 7Site LLC — Trinity Infinity Geometry
 * Authors: Brayden Ross Sanders & Monica
 */

`default_nettype none

module ck_top_gen12 (
    input  wire        pl_clk_50m,        // 50 MHz PL oscillator (U18)

    // LEDs (active-low)
    output wire        led1_n,            // Δ⁰ heartbeat pulse (R19)
    output wire        led2_n,            // Δ³ HELD indicator — solid at T* (V13)

    // Reset / nudge
    input  wire        key1_n,            // Reset (G14, active-low)
    input  wire        key2_n,            // Nudge heartbeat (J15, active-low)

    // HDMI output (TMDS differential, Bank 34)
    output wire        hdmi_clk_p,
    output wire        hdmi_clk_n,
    output wire [2:0]  hdmi_data_p,
    output wire [2:0]  hdmi_data_n,
    output wire        hdmi_out_en,
    input  wire        hdmi_hpd,
    output wire        hdmi_scl,
    inout  wire        hdmi_sda,

    // JM1: LCD output (32 IOs)
    output wire [31:0] jm1,

    // JM2: servo TX
    input  wire [30:0] jm2,
    output wire        jm2_servo_tx,      // Y14 — servo UART TX to XiaoR

    // JM2 UART RX from R16 (leash)
    // Pin assignment: use spare JM2 input (jm2[0])
    // This is the Δ¹ line — R16 ↔ FPGA
    // Note: for full duplex leash, wire jm2[0] to R16 TX output
    input  wire        jm2_leash_rx,      // jm2[0] — R16 → FPGA command RX

    // PL Gigabit Ethernet RGMII (Bank 34, RTL8211F-CG)
    output wire        pl_eth_gtx_clk,
    output wire [3:0]  pl_eth_txd,
    output wire        pl_eth_tx_en,
    output wire        pl_eth_mdc,
    inout  wire        pl_eth_mdio
);

    // =========================================================
    // Clock and Reset
    // =========================================================

    wire clk = pl_clk_50m;

    // Key synchronizers (active-low → active-high)
    reg [3:0] key1_sync, key2_sync;
    always @(posedge clk) begin
        key1_sync <= {key1_sync[2:0], ~key1_n};
        key2_sync <= {key2_sync[2:0], ~key2_n};
    end
    wire key1_pressed = key1_sync[3];
    wire key2_pressed = key2_sync[3] & ~key2_sync[2];  // rising edge

    // Power-on reset + key reset
    reg [7:0] por_cnt;
    reg       rst_n;
    always @(posedge clk) begin
        if (key1_pressed) begin
            por_cnt <= 8'd0;
            rst_n   <= 1'b0;
        end else if (!rst_n) begin
            if (por_cnt == 8'hFF)
                rst_n <= 1'b1;
            else
                por_cnt <= por_cnt + 8'd1;
        end
    end

    // =========================================================
    // Δ⁰ — Heartbeat (50Hz CK tick)
    // =========================================================
    // The heartbeat is the point. It is the only thing that
    // exists before the leash is drawn.

    wire        tick_done;
    wire [31:0] tick_count;
    wire [3:0]  fuse_op;
    wire [3:0]  phase_bc;
    wire [15:0] coh_num;
    wire [15:0] coh_den;
    wire        bump;
    wire [15:0] leg_op_flat;

    // CK heartbeat: CL composition table, 50Hz, coherence accumulation
    // (reuse existing ck_heartbeat module from Gen9)
    ck_heartbeat #(
        .CLK_FREQ(50_000_000),
        .TICK_HZ (50)
    ) heartbeat_inst (
        .clk        (clk),
        .rst_n      (rst_n),
        .nudge      (key2_pressed),
        .tick_done  (tick_done),
        .tick_count (tick_count),
        .fuse_op    (fuse_op),
        .phase_bc   (phase_bc),
        .coh_num    (coh_num),
        .coh_den    (coh_den),
        .bump       (bump),
        .leg_op_flat(leg_op_flat)
    );

    // =========================================================
    // Δ² — HD Gap: Exact Simplex Thresholds
    // =========================================================
    // 1/2 and 5/7 computed by cross-multiplication. No division.
    // This is the geometry in silicon.

    wire [1:0]  simplex_state;   // 00=Δ⁰void 01=Δ¹estop 10=Δ²gap 11=Δ³held
    wire [15:0] gap_position;    // HD position within [1/2, 5/7)
    wire        gap_valid;
    wire        is_void, is_gap, is_held, is_estop;

    coherence_gap #(.W(16)) gap_inst (
        .clk          (clk),
        .rst_n        (rst_n),
        .valid_in     (tick_done),
        .coh_num      (coh_num),
        .coh_den      (coh_den),
        // E-STOP floor: coh < 1/5 = 0.20
        .estop_num    (16'd1),
        .estop_den    (16'd5),
        .simplex_state(simplex_state),
        .gap_position (gap_position),
        .state_valid  (gap_valid),
        .is_void      (is_void),
        .is_gap       (is_gap),
        .is_held      (is_held),
        .is_estop     (is_estop)
    );

    // =========================================================
    // Δ³ — Gait: Dog Locomotion
    // =========================================================
    // simplex_state → gait_mode → servo positions → XiaoR

    // Map simplex state to gait mode
    // Δ⁰ (void) → STAND (0)
    // Δ¹ (estop)→ STAND (0) with E-STOP servo center
    // Δ² (gap)  → WALK  (1)
    // Δ³ (held) → TROT  (2)
    reg [1:0] gait_mode;
    reg       gait_estop;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            gait_mode  <= 2'd0;
            gait_estop <= 1'b1;
        end else if (gap_valid) begin
            gait_estop <= is_estop;
            case (simplex_state)
                2'b00: gait_mode <= 2'd0;  // Δ⁰ void → STAND
                2'b01: gait_mode <= 2'd0;  // Δ¹ estop → STAND (servos safe)
                2'b10: gait_mode <= 2'd1;  // Δ² gap → WALK
                2'b11: gait_mode <= 2'd2;  // Δ³ held → TROT
            endcase
        end
    end

    // Gait vortex: torus CL computation for 4-leg coordination
    wire [15:0] vortex_flat;
    wire [3:0]  aligned_flat;
    wire        all_aligned;
    wire [15:0] correction_op_flat;
    wire        correction_valid;
    wire [15:0] gait_coh_num, gait_coh_den;
    wire [31:0] gait_tick_count;
    wire [3:0]  gait_phase;

    gait_vortex #(.CLK_FREQ(50_000_000)) gait_inst (
        .clk              (clk),
        .rst_n            (rst_n),
        .enable           (~gait_estop),
        .heartbeat_tick   (tick_done),
        .gait_mode        (gait_mode),
        .gait_start       (gap_valid),
        .leg_op_flat      (leg_op_flat),
        .vortex_flat      (vortex_flat),
        .aligned_flat     (aligned_flat),
        .delta_flat       (),
        .all_aligned      (all_aligned),
        .correction_op_flat(correction_op_flat),
        .correction_valid (correction_valid),
        .gait_coherence_num(gait_coh_num),
        .gait_coherence_den(gait_coh_den),
        .gait_tick_count  (gait_tick_count),
        .gait_phase       (gait_phase)
    );

    // Servo commander: corrections → 8x LewanSoul LX servo positions
    // Two UART TX sources share the bus (AND: both idle-high, activity pulls low)
    wire        servo_tx_i;    // from servo_commander
    wire        leash_tx_i;    // from ck_leash_rx

    servo_commander servo_inst (
        .clk              (clk),
        .rst_n            (rst_n),
        .correction_op    (correction_op_flat),
        .correction_valid (correction_valid & ~gait_estop),
        .gait_mode        (gait_mode),
        .estop            (gait_estop),
        .servo_tx         (servo_tx_i)
    );

    // Shared UART bus: idle-high lines AND together (activity = low)
    assign jm2_servo_tx = servo_tx_i & leash_tx_i;

    // =========================================================
    // Δ¹ — Leash UART RX (R16 → FPGA)
    // =========================================================
    // Simple command receiver. Parses PING/OBSERVE/GAIT/ESTOP packets.
    // Sends STATE packets back via servo_uart_tx (shared bus, different time slot).
    // This is the line between R16 (brain) and FPGA (body).
    //
    // Gen12.00: RX parsed, gait_mode override from R16 command added.
    // Full duplex requires level shifter on JM2 spare pin → R16 COM port.

    wire [1:0] r16_gait_cmd;
    wire       r16_gait_valid;
    wire       r16_estop_cmd;

    ck_leash_rx #(
        .CLK_FREQ(50_000_000),
        .BAUD    (115200)
    ) leash_rx_inst (
        .clk          (clk),
        .rst_n        (rst_n),
        .uart_rx      (jm2_leash_rx),
        .gait_cmd     (r16_gait_cmd),
        .gait_valid   (r16_gait_valid),
        .estop_cmd    (r16_estop_cmd),
        .coh_num_in   (coh_num),
        .coh_den_in   (coh_den),
        .tick_in      (tick_count),
        .simplex_in   (simplex_state),
        .tx_out       (leash_tx_i)    // Δ¹ PONG response, AND'd with servo_tx_i
    );

    // =========================================================
    // Δ¹ — PL Ethernet: Coherence Streaming (HD Gap payload)
    // =========================================================
    // Payload extended from Gen11 (10 bytes) to Gen12 (12 bytes).
    // gap_position added: HD position within the Δ² bridge zone.

    wire mmcm_locked;
    wire link_ready;

    ck_eth_tx_gen12 eth_inst (
        .clk_50m      (clk),
        .rst_n        (rst_n),
        // Heartbeat inputs
        .tick_done    (tick_done),
        .tick_count   (tick_count),
        // Gen12 HD gap payload
        .simplex_state(simplex_state),   // 2 bits: which Δ layer
        .gap_position (gap_position),    // 16 bits: HD position in bridge
        .fuse_op      (fuse_op),
        .coh_num      (coh_num),
        .coh_den      (coh_den),
        .bump         (bump),
        // RGMII PHY
        .phy_gtx_clk  (pl_eth_gtx_clk),
        .phy_txd      (pl_eth_txd),
        .phy_tx_en    (pl_eth_tx_en),
        .phy_mdc      (pl_eth_mdc),
        .phy_mdio     (pl_eth_mdio),
        .mmcm_locked  (mmcm_locked),
        .link_ready   (link_ready)
    );

    // =========================================================
    // LED indicators
    // =========================================================
    // LED1: heartbeat pulse (Δ⁰ — the point exists)
    // LED2: Δ³ HELD — solid when T* is crossed (TROT)

    reg led1_r, led2_r;
    reg [19:0] led1_stretch;  // Stretch heartbeat pulse for visibility

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            led1_r       <= 1'b0;
            led2_r       <= 1'b0;
            led1_stretch <= 20'd0;
        end else begin
            if (tick_done)
                led1_stretch <= 20'hFFFFF;  // ~20ms stretch at 50MHz
            else if (led1_stretch != 20'd0)
                led1_stretch <= led1_stretch - 20'd1;
            led1_r <= (led1_stretch != 20'd0);
            led2_r <= is_held;  // Solid at T* — the geometry holds
        end
    end

    assign led1_n = ~led1_r;
    assign led2_n = ~led2_r;

    // =========================================================
    // HDMI / LCD (reuse from Gen11 — face unchanged)
    // =========================================================
    ck_hdmi_out hdmi_inst (
        .clk          (clk),
        .rst_n        (rst_n),
        .fuse_op      (fuse_op),
        .coh_num      (coh_num),
        .coh_den      (coh_den),
        .tick_count   (tick_count),
        .simplex_state(simplex_state),   // Gen12: show Δ layer on face
        .hdmi_clk_p   (hdmi_clk_p),
        .hdmi_clk_n   (hdmi_clk_n),
        .hdmi_data_p  (hdmi_data_p),
        .hdmi_data_n  (hdmi_data_n),
        .hdmi_out_en  (hdmi_out_en),
        .hdmi_hpd     (hdmi_hpd),
        .hdmi_scl     (hdmi_scl),
        .hdmi_sda     (hdmi_sda),
        .jm1          (jm1)
    );

    // Unused inputs
    wire _unused = &{jm2[30:1], key2_n};

endmodule

`default_nettype wire
