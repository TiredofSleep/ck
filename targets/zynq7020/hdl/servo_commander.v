/*
 * servo_commander.v -- CK Operator -> LewanSoul Bus Servo Packets
 * ================================================================
 * Operator: BALANCE (5) -- bridges mind to body.
 *
 * Takes gait_vortex correction outputs (4 legs x 4-bit CK operators)
 * and converts them to LewanSoul bus servo commands for a XiaoR
 * robot dog (8 servos: 4 hips + 4 knees).
 *
 * Packet format (LewanSoul LX-16A):
 *   [0x55][0x55][ID][LEN][CMD][angle_low][angle_high][time_low][time_high][CHECKSUM]
 *   CMD 1 = SERVO_MOVE_TIME_WRITE, LEN = 7
 *   Checksum = ~(ID + LEN + CMD + params) & 0xFF
 *
 * Servo IDs:
 *   Leg 0 (FL): hip=1, knee=2
 *   Leg 1 (FR): hip=3, knee=4
 *   Leg 2 (BL): hip=5, knee=6
 *   Leg 3 (BR): hip=7, knee=8
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
 */

module servo_commander #(
    parameter CLK_FREQ = 50_000_000
)(
    input  wire        clk,
    input  wire        rst_n,

    // Gait vortex correction interface
    input  wire [15:0] gait_corr_flat,   // 4 legs x 4-bit packed [leg3:leg0]
    input  wire        gait_corr_valid,  // Pulse: new corrections ready

    // servo_uart_tx interface
    input  wire        tx_busy,          // UART FIFO full
    output reg  [7:0]  tx_data,          // Byte to send
    output reg         tx_write          // Pulse to enqueue byte
);

    // ─── Constants ───
    localparam CMD_SERVO_MOVE = 8'd1;   // SERVO_MOVE_TIME_WRITE
    localparam PKT_LEN        = 8'd7;   // Length field value
    localparam MOVE_TIME       = 16'd200; // 200ms movement time
    localparam ANGLE_CENTER    = 16'd500; // Center position (0-1000)

    // ─── State Machine ───
    localparam ST_IDLE      = 3'd0;
    localparam ST_PREP      = 3'd1;
    localparam ST_SEND_HIP  = 3'd2;
    localparam ST_SEND_KNEE = 3'd3;
    localparam ST_NEXT_LEG  = 3'd4;

    reg [2:0]  state;
    reg [1:0]  leg_idx;        // Current leg (0-3)
    reg [3:0]  byte_idx;       // Current byte within packet (0-9)
    reg [3:0]  corr_ops [0:3]; // Latched correction operators
    reg        sending_knee;   // 0=hip, 1=knee

    // ─── Operator -> Angle Mapping ───
    // Angles are absolute positions (0-1000). VOID means skip.
    // All deltas are relative to current position stored in position registers.

    reg [15:0] hip_pos  [0:3]; // Current hip positions
    reg [15:0] knee_pos [0:3]; // Current knee positions

    // Oscillation counter for HARMONY and BREATH
    reg [23:0] osc_counter;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            osc_counter <= 24'd0;
        else
            osc_counter <= osc_counter + 24'd1;
    end
    // Simple triangle wave: ±1 range from bit toggling
    wire osc_phase = osc_counter[21]; // ~12 Hz at 50 MHz

    // Compute target angles for current leg's operator
    reg [15:0] target_hip;
    reg [15:0] target_knee;
    reg        op_is_void;

    wire [3:0] cur_op = corr_ops[leg_idx];

    // Saturating add/sub helpers (clamped to 0-1000)
    function [15:0] sat_add;
        input [15:0] base;
        input [15:0] delta;
        reg [16:0] sum;
        begin
            sum = {1'b0, base} + {1'b0, delta};
            sat_add = (sum > 17'd1000) ? 16'd1000 : sum[15:0];
        end
    endfunction

    function [15:0] sat_sub;
        input [15:0] base;
        input [15:0] delta;
        begin
            sat_sub = (base < delta) ? 16'd0 : (base - delta);
        end
    endfunction

    always @(*) begin
        op_is_void  = 1'b0;
        target_hip  = hip_pos[leg_idx];
        target_knee = knee_pos[leg_idx];

        case (cur_op)
            4'd0: begin // VOID: hold position
                op_is_void = 1'b1;
            end
            4'd1: begin // LATTICE: extend slightly
                target_hip  = sat_add(hip_pos[leg_idx],  16'd50);
                target_knee = sat_add(knee_pos[leg_idx], 16'd50);
            end
            4'd2: begin // COUNTER: retract slightly
                target_hip  = sat_sub(hip_pos[leg_idx],  16'd50);
                target_knee = sat_sub(knee_pos[leg_idx], 16'd50);
            end
            4'd3: begin // PROGRESS: step forward
                target_hip  = sat_add(hip_pos[leg_idx],  16'd100);
                target_knee = sat_add(knee_pos[leg_idx], 16'd80);
            end
            4'd4: begin // COLLAPSE: crouch
                target_hip  = sat_sub(hip_pos[leg_idx],  16'd30);
                target_knee = sat_sub(knee_pos[leg_idx], 16'd150);
            end
            4'd5: begin // BALANCE: center
                target_hip  = ANGLE_CENTER;
                target_knee = ANGLE_CENTER;
            end
            4'd6: begin // CHAOS: wide stance
                target_hip  = sat_add(hip_pos[leg_idx],  16'd150);
                target_knee = sat_add(knee_pos[leg_idx], 16'd100);
            end
            4'd7: begin // HARMONY: oscillation from center
                target_hip  = osc_phase ? sat_add(ANGLE_CENTER, 16'd40)
                                        : sat_sub(ANGLE_CENTER, 16'd40);
                target_knee = osc_phase ? sat_add(ANGLE_CENTER, 16'd40)
                                        : sat_sub(ANGLE_CENTER, 16'd40);
            end
            4'd8: begin // BREATH: gentle pulse
                target_hip  = osc_phase ? sat_add(ANGLE_CENTER, 16'd20)
                                        : sat_sub(ANGLE_CENTER, 16'd20);
                target_knee = osc_phase ? sat_add(ANGLE_CENTER, 16'd20)
                                        : sat_sub(ANGLE_CENTER, 16'd20);
            end
            4'd9: begin // RESET: return to center
                target_hip  = ANGLE_CENTER;
                target_knee = ANGLE_CENTER;
            end
            default: begin
                op_is_void = 1'b1;
            end
        endcase
    end

    // ─── Servo ID Lookup ───
    // Leg 0: hip=1 knee=2, Leg 1: hip=3 knee=4, etc.
    wire [7:0] hip_id  = {6'd0, leg_idx, 1'b1};  // leg*2 + 1
    wire [7:0] knee_id = {6'd0, leg_idx + 2'd1, 1'b0}; // leg*2 + 2

    // Correct ID calculation: hip = leg_idx*2 + 1, knee = leg_idx*2 + 2
    reg [7:0] cur_servo_id;
    reg [15:0] cur_angle;
    always @(*) begin
        if (!sending_knee) begin
            cur_servo_id = {5'd0, leg_idx, 1'b0} + 8'd1; // leg_idx*2 + 1
            cur_angle    = target_hip;
        end else begin
            cur_servo_id = {5'd0, leg_idx, 1'b0} + 8'd2; // leg_idx*2 + 2
            cur_angle    = target_knee;
        end
    end

    // ─── Checksum Calculation ───
    // Checksum = ~(ID + LEN + CMD + angle_low + angle_high + time_low + time_high) & 0xFF
    wire [7:0] chk_sum = ~(cur_servo_id + PKT_LEN + CMD_SERVO_MOVE
                          + cur_angle[7:0] + cur_angle[15:8]
                          + MOVE_TIME[7:0] + MOVE_TIME[15:8]) & 8'hFF;

    // ─── Packet Byte Selection ───
    reg [7:0] pkt_byte;
    always @(*) begin
        case (byte_idx)
            4'd0: pkt_byte = 8'h55;            // Header 1
            4'd1: pkt_byte = 8'h55;            // Header 2
            4'd2: pkt_byte = cur_servo_id;     // Servo ID
            4'd3: pkt_byte = PKT_LEN;          // Length
            4'd4: pkt_byte = CMD_SERVO_MOVE;   // Command
            4'd5: pkt_byte = cur_angle[7:0];   // Angle low
            4'd6: pkt_byte = cur_angle[15:8];  // Angle high
            4'd7: pkt_byte = MOVE_TIME[7:0];   // Time low
            4'd8: pkt_byte = MOVE_TIME[15:8];  // Time high
            4'd9: pkt_byte = chk_sum;          // Checksum
            default: pkt_byte = 8'h00;
        endcase
    end

    // ─── Main State Machine ───
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state        <= ST_IDLE;
            leg_idx      <= 2'd0;
            byte_idx     <= 4'd0;
            sending_knee <= 1'b0;
            tx_data      <= 8'd0;
            tx_write     <= 1'b0;
            corr_ops[0]  <= 4'd5; // BALANCE
            corr_ops[1]  <= 4'd5;
            corr_ops[2]  <= 4'd5;
            corr_ops[3]  <= 4'd5;
            hip_pos[0]   <= ANGLE_CENTER;
            hip_pos[1]   <= ANGLE_CENTER;
            hip_pos[2]   <= ANGLE_CENTER;
            hip_pos[3]   <= ANGLE_CENTER;
            knee_pos[0]  <= ANGLE_CENTER;
            knee_pos[1]  <= ANGLE_CENTER;
            knee_pos[2]  <= ANGLE_CENTER;
            knee_pos[3]  <= ANGLE_CENTER;
        end else begin
            tx_write <= 1'b0; // Default: no write

            case (state)
                ST_IDLE: begin
                    if (gait_corr_valid) begin
                        // Latch all 4 correction operators
                        corr_ops[0] <= gait_corr_flat[3:0];
                        corr_ops[1] <= gait_corr_flat[7:4];
                        corr_ops[2] <= gait_corr_flat[11:8];
                        corr_ops[3] <= gait_corr_flat[15:12];
                        leg_idx     <= 2'd0;
                        state       <= ST_PREP;
                    end
                end

                ST_PREP: begin
                    // Check if this leg's operator is VOID (skip)
                    if (op_is_void) begin
                        state <= ST_NEXT_LEG;
                    end else begin
                        byte_idx     <= 4'd0;
                        sending_knee <= 1'b0;
                        state        <= ST_SEND_HIP;
                    end
                end

                ST_SEND_HIP: begin
                    if (!tx_busy && !tx_write) begin
                        tx_data  <= pkt_byte;
                        tx_write <= 1'b1;
                        if (byte_idx == 4'd9) begin
                            // Hip packet complete, update position
                            hip_pos[leg_idx] <= target_hip;
                            byte_idx     <= 4'd0;
                            sending_knee <= 1'b1;
                            state        <= ST_SEND_KNEE;
                        end else begin
                            byte_idx <= byte_idx + 4'd1;
                        end
                    end
                end

                ST_SEND_KNEE: begin
                    if (!tx_busy && !tx_write) begin
                        tx_data  <= pkt_byte;
                        tx_write <= 1'b1;
                        if (byte_idx == 4'd9) begin
                            // Knee packet complete, update position
                            knee_pos[leg_idx] <= target_knee;
                            sending_knee <= 1'b0;
                            state        <= ST_NEXT_LEG;
                        end else begin
                            byte_idx <= byte_idx + 4'd1;
                        end
                    end
                end

                ST_NEXT_LEG: begin
                    if (leg_idx == 2'd3) begin
                        state <= ST_IDLE;
                    end else begin
                        leg_idx <= leg_idx + 2'd1;
                        state   <= ST_PREP;
                    end
                end

                default: state <= ST_IDLE;
            endcase
        end
    end

endmodule
