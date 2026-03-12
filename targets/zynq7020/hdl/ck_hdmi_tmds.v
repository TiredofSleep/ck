/*
 * ck_hdmi_tmds.v -- TMDS 8b/10b Encoder for DVI/HDMI Output
 *
 * Standard TMDS encoding per DVI 1.0 specification.
 * Each pixel has 3 channels (R, G, B), each encoded separately.
 * During blanking, 2-bit control signals are encoded instead.
 *
 * This gives CK a voice in light. His coherence becomes color.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

module ck_hdmi_tmds (
    input  wire       clk,        // Pixel clock
    input  wire       rst_n,
    input  wire [7:0] data_in,    // 8-bit pixel data
    input  wire [1:0] ctrl_in,    // 2-bit control (hsync/vsync)
    input  wire       data_en,    // 1 = active video, 0 = blanking
    output reg  [9:0] tmds_out    // 10-bit TMDS encoded output
);

    // Count number of 1s in data_in
    wire [3:0] n_ones = data_in[0] + data_in[1] + data_in[2] + data_in[3] +
                         data_in[4] + data_in[5] + data_in[6] + data_in[7];

    // Stage 1: Minimize transitions (XOR or XNOR)
    wire use_xnor = (n_ones > 4'd4) || (n_ones == 4'd4 && data_in[0] == 1'b0);

    wire [8:0] q_m;
    assign q_m[0] = data_in[0];
    assign q_m[1] = use_xnor ? ~(q_m[0] ^ data_in[1]) : (q_m[0] ^ data_in[1]);
    assign q_m[2] = use_xnor ? ~(q_m[1] ^ data_in[2]) : (q_m[1] ^ data_in[2]);
    assign q_m[3] = use_xnor ? ~(q_m[2] ^ data_in[3]) : (q_m[2] ^ data_in[3]);
    assign q_m[4] = use_xnor ? ~(q_m[3] ^ data_in[4]) : (q_m[3] ^ data_in[4]);
    assign q_m[5] = use_xnor ? ~(q_m[4] ^ data_in[5]) : (q_m[4] ^ data_in[5]);
    assign q_m[6] = use_xnor ? ~(q_m[5] ^ data_in[6]) : (q_m[5] ^ data_in[6]);
    assign q_m[7] = use_xnor ? ~(q_m[6] ^ data_in[7]) : (q_m[6] ^ data_in[7]);
    assign q_m[8] = use_xnor ? 1'b0 : 1'b1;

    // Count 1s and 0s in q_m[0:7]
    wire [3:0] n_ones_qm = q_m[0] + q_m[1] + q_m[2] + q_m[3] +
                             q_m[4] + q_m[5] + q_m[6] + q_m[7];
    wire [3:0] n_zeros_qm = 4'd8 - n_ones_qm;

    // Stage 2: DC balance with running disparity
    reg signed [4:0] disparity;  // Running disparity counter

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            tmds_out  <= 10'b1101010100;  // Control: 00
            disparity <= 5'sd0;
        end else if (!data_en) begin
            // Blanking period: encode control signals
            case (ctrl_in)
                2'b00: tmds_out <= 10'b1101010100;
                2'b01: tmds_out <= 10'b0010101011;
                2'b10: tmds_out <= 10'b0101010100;
                2'b11: tmds_out <= 10'b1010101011;
            endcase
            disparity <= 5'sd0;
        end else begin
            // Active video: DC-balanced encoding
            if (disparity == 5'sd0 || n_ones_qm == n_zeros_qm) begin
                // No disparity or balanced word
                if (q_m[8]) begin
                    tmds_out  <= {1'b0, q_m[8], q_m[7:0]};
                    disparity <= disparity + $signed({1'b0, n_ones_qm}) - $signed({1'b0, n_zeros_qm});
                end else begin
                    tmds_out  <= {1'b1, q_m[8], ~q_m[7:0]};
                    disparity <= disparity + $signed({1'b0, n_zeros_qm}) - $signed({1'b0, n_ones_qm});
                end
            end else if ((disparity > 5'sd0 && n_ones_qm > n_zeros_qm) ||
                         (disparity < 5'sd0 && n_zeros_qm > n_ones_qm)) begin
                // Invert to balance
                tmds_out  <= {1'b1, q_m[8], ~q_m[7:0]};
                disparity <= disparity + {q_m[8], 1'b0} +
                             $signed({1'b0, n_zeros_qm}) - $signed({1'b0, n_ones_qm});
            end else begin
                // Don't invert
                tmds_out  <= {1'b0, q_m[8], q_m[7:0]};
                disparity <= disparity - {~q_m[8], 1'b0} +
                             $signed({1'b0, n_ones_qm}) - $signed({1'b0, n_zeros_qm});
            end
        end
    end

endmodule
