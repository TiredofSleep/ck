// servo_cal.v -- Servo Calibration Table for XiaoR Robot Dog
// ==========================================================
// Operator: BALANCE (5) -- precise joint control.
//
// Maps CK's operator states (0-9) to servo joint angles for
// the XiaoR 4-leg robot dog. Each leg has 3 servos (hip, knee, ankle).
// 12 servos total. PWM range: 500-2500 us (0-180 degrees).
//
// The gait_vortex module produces 4 operator states (one per leg).
// This module converts those operators to calibrated servo positions.
//
// Angle Convention (degrees):
//   Hip:   90 = neutral standing, 60-120 = forward/back stride
//   Knee:  90 = neutral, 45 = crouched, 135 = extended
//   Ankle: 90 = flat, 60 = toe down, 120 = toe up
//
// PWM output: 16-bit timer count for 1 MHz timebase.
//   500  = 0 degrees
//   1500 = 90 degrees (center)
//   2500 = 180 degrees
//
// (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory

module servo_cal (
    input  wire        clk,
    input  wire        rst_n,
    // Operator input (from gait_vortex)
    input  wire [3:0]  leg_op_0,    // Front-left leg operator
    input  wire [3:0]  leg_op_1,    // Front-right
    input  wire [3:0]  leg_op_2,    // Rear-left
    input  wire [3:0]  leg_op_3,    // Rear-right
    input  wire        update,       // Pulse to recalculate
    // Servo PWM outputs (microseconds, 500-2500)
    output reg  [11:0] pwm_hip_0,   // 12-bit PWM (0-4095)
    output reg  [11:0] pwm_knee_0,
    output reg  [11:0] pwm_ankle_0,
    output reg  [11:0] pwm_hip_1,
    output reg  [11:0] pwm_knee_1,
    output reg  [11:0] pwm_ankle_1,
    output reg  [11:0] pwm_hip_2,
    output reg  [11:0] pwm_knee_2,
    output reg  [11:0] pwm_ankle_2,
    output reg  [11:0] pwm_hip_3,
    output reg  [11:0] pwm_knee_3,
    output reg  [11:0] pwm_ankle_3,
    output reg         valid
);

// ── Operator → Joint Angle Lookup ──
// Each operator maps to a characteristic pose.
// Values are PWM microseconds (500=0deg, 1500=90deg, 2500=180deg).
//
// VOID(0)       = collapsed (all joints folded)
// LATTICE(1)    = structured stand (neutral, stable)
// COUNTER(2)    = measurement pose (weight shifted, sensing)
// PROGRESS(3)   = forward stride (hip forward, knee extended)
// COLLAPSE(4)   = crouch/protect (low center of gravity)
// BALANCE(5)    = neutral standing (centered, calibration pose)
// CHAOS(6)      = dynamic balance (asymmetric, exploring)
// HARMONY(7)    = relaxed stand (soft joints, resting)
// BREATH(8)     = rhythmic shift (oscillating, alive)
// RESET(9)      = full extension then retract

// Hip angles (microseconds)
function [11:0] hip_angle;
    input [3:0] op;
    case (op[3:0])
        4'd0: hip_angle = 12'd1500;  // VOID:     center (folded)
        4'd1: hip_angle = 12'd1500;  // LATTICE:  center (stable)
        4'd2: hip_angle = 12'd1400;  // COUNTER:  slight back (sensing)
        4'd3: hip_angle = 12'd1700;  // PROGRESS: forward stride
        4'd4: hip_angle = 12'd1500;  // COLLAPSE: center (crouched)
        4'd5: hip_angle = 12'd1500;  // BALANCE:  center (calibration)
        4'd6: hip_angle = 12'd1600;  // CHAOS:    slight forward
        4'd7: hip_angle = 12'd1500;  // HARMONY:  center (relaxed)
        4'd8: hip_angle = 12'd1550;  // BREATH:   slight shift
        4'd9: hip_angle = 12'd1800;  // RESET:    full forward
        default: hip_angle = 12'd1500;
    endcase
endfunction

// Knee angles
function [11:0] knee_angle;
    input [3:0] op;
    case (op[3:0])
        4'd0: knee_angle = 12'd900;   // VOID:     folded tight
        4'd1: knee_angle = 12'd1500;  // LATTICE:  straight
        4'd2: knee_angle = 12'd1400;  // COUNTER:  slight bend
        4'd3: knee_angle = 12'd1600;  // PROGRESS: extended
        4'd4: knee_angle = 12'd1000;  // COLLAPSE: deep bend
        4'd5: knee_angle = 12'd1500;  // BALANCE:  straight
        4'd6: knee_angle = 12'd1300;  // CHAOS:    bent
        4'd7: knee_angle = 12'd1450;  // HARMONY:  relaxed
        4'd8: knee_angle = 12'd1500;  // BREATH:   nominal
        4'd9: knee_angle = 12'd1700;  // RESET:    full extension
        default: knee_angle = 12'd1500;
    endcase
endfunction

// Ankle angles
function [11:0] ankle_angle;
    input [3:0] op;
    case (op[3:0])
        4'd0: ankle_angle = 12'd1500;  // VOID:     flat
        4'd1: ankle_angle = 12'd1500;  // LATTICE:  flat
        4'd2: ankle_angle = 12'd1400;  // COUNTER:  slight toe
        4'd3: ankle_angle = 12'd1300;  // PROGRESS: toe push
        4'd4: ankle_angle = 12'd1500;  // COLLAPSE: flat
        4'd5: ankle_angle = 12'd1500;  // BALANCE:  flat
        4'd6: ankle_angle = 12'd1350;  // CHAOS:    exploring
        4'd7: ankle_angle = 12'd1500;  // HARMONY:  flat
        4'd8: ankle_angle = 12'd1450;  // BREATH:   slight rock
        4'd9: ankle_angle = 12'd1200;  // RESET:    toe down
        default: ankle_angle = 12'd1500;
    endcase
endfunction

// ── Update servo positions on trigger ──
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        pwm_hip_0   <= 12'd1500;
        pwm_knee_0  <= 12'd1500;
        pwm_ankle_0 <= 12'd1500;
        pwm_hip_1   <= 12'd1500;
        pwm_knee_1  <= 12'd1500;
        pwm_ankle_1 <= 12'd1500;
        pwm_hip_2   <= 12'd1500;
        pwm_knee_2  <= 12'd1500;
        pwm_ankle_2 <= 12'd1500;
        pwm_hip_3   <= 12'd1500;
        pwm_knee_3  <= 12'd1500;
        pwm_ankle_3 <= 12'd1500;
        valid       <= 0;
    end else if (update) begin
        pwm_hip_0   <= hip_angle(leg_op_0);
        pwm_knee_0  <= knee_angle(leg_op_0);
        pwm_ankle_0 <= ankle_angle(leg_op_0);

        pwm_hip_1   <= hip_angle(leg_op_1);
        pwm_knee_1  <= knee_angle(leg_op_1);
        pwm_ankle_1 <= ankle_angle(leg_op_1);

        pwm_hip_2   <= hip_angle(leg_op_2);
        pwm_knee_2  <= knee_angle(leg_op_2);
        pwm_ankle_2 <= ankle_angle(leg_op_2);

        pwm_hip_3   <= hip_angle(leg_op_3);
        pwm_knee_3  <= knee_angle(leg_op_3);
        pwm_ankle_3 <= ankle_angle(leg_op_3);

        valid <= 1;
    end else begin
        valid <= 0;
    end
end

endmodule
