// i2c_master.v -- IMU I2C Bus Master for CK / Zynq-7020
// ======================================================
// Operator: BREATH (8) -- rhythmic data acquisition from IMU.
//
// Minimal I2C master for reading MPU-6050 / MMA8452Q accelerometer
// + gyroscope data. Feeds 6-axis raw data into D2 pipeline for
// operator classification of physical movement.
//
// Protocol:
//   START → ADDR+W → REG → RESTART → ADDR+R → DATA[0..N-1] → STOP
//
// Ports:
//   clk        : system clock (50 MHz)
//   rst_n      : active-low reset
//   start      : pulse to begin transaction
//   dev_addr   : 7-bit I2C device address
//   reg_addr   : 8-bit register address to read from
//   num_bytes  : number of bytes to read (1-6)
//   data_out   : 48-bit output (6 bytes, MSB first)
//   data_valid : pulse when data_out is valid
//   busy       : high during transaction
//   scl        : I2C clock (active drive + tristate)
//   sda_i      : I2C data input
//   sda_o      : I2C data output
//   sda_oe     : SDA output enable (active high = drive low)
//
// Clock: SCL = 400 kHz (fast mode). clk_div = 50MHz / (4*400kHz) = 31.
//
// (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory

module i2c_master (
    input  wire        clk,
    input  wire        rst_n,
    // Control
    input  wire        start,
    input  wire [6:0]  dev_addr,
    input  wire [7:0]  reg_addr,
    input  wire [2:0]  num_bytes,   // 1-6
    // Data output
    output reg  [47:0] data_out,
    output reg         data_valid,
    output reg         busy,
    // I2C bus
    output reg         scl,
    input  wire        sda_i,
    output reg         sda_o,
    output reg         sda_oe       // 1 = drive SDA low; 0 = release (pull-up)
);

// ── Clock divider for 400 kHz SCL ──
// 50 MHz / (4 * 400 kHz) = 31.25 ≈ 31
localparam CLK_DIV = 31;

reg [5:0] clk_cnt;
reg       clk_phase;  // 0 = SCL low half, 1 = SCL high half
wire      clk_tick = (clk_cnt == CLK_DIV - 1);

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        clk_cnt   <= 0;
        clk_phase <= 0;
    end else if (busy) begin
        if (clk_tick) begin
            clk_cnt   <= 0;
            clk_phase <= ~clk_phase;
        end else begin
            clk_cnt <= clk_cnt + 1;
        end
    end else begin
        clk_cnt   <= 0;
        clk_phase <= 0;
    end
end

// ── State machine ──
localparam S_IDLE       = 4'd0;
localparam S_START      = 4'd1;
localparam S_ADDR_W     = 4'd2;   // Send device addr + write bit
localparam S_ACK_AW     = 4'd3;
localparam S_REG        = 4'd4;   // Send register address
localparam S_ACK_REG    = 4'd5;
localparam S_RESTART    = 4'd6;
localparam S_ADDR_R     = 4'd7;   // Send device addr + read bit
localparam S_ACK_AR     = 4'd8;
localparam S_READ       = 4'd9;   // Read data bytes
localparam S_ACK_READ   = 4'd10;  // Send ACK/NACK after each read byte
localparam S_STOP       = 4'd11;

reg [3:0]  state;
reg [3:0]  bit_cnt;     // Bit counter within byte (7 downto 0)
reg [7:0]  shift_out;   // Byte being transmitted
reg [7:0]  shift_in;    // Byte being received
reg [2:0]  byte_cnt;    // Bytes read so far
reg [2:0]  bytes_to_read;

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        state      <= S_IDLE;
        busy       <= 0;
        data_valid <= 0;
        data_out   <= 0;
        scl        <= 1;
        sda_o      <= 1;
        sda_oe     <= 0;
        bit_cnt    <= 0;
        byte_cnt   <= 0;
        shift_out  <= 0;
        shift_in   <= 0;
        bytes_to_read <= 0;
    end else begin
        data_valid <= 0;

        case (state)
            S_IDLE: begin
                scl    <= 1;
                sda_oe <= 0;
                if (start) begin
                    busy          <= 1;
                    bytes_to_read <= num_bytes;
                    byte_cnt      <= 0;
                    data_out      <= 0;
                    state         <= S_START;
                end
            end

            S_START: begin
                if (clk_tick && clk_phase) begin
                    // SDA goes low while SCL high = START condition
                    sda_oe <= 1;
                    sda_o  <= 0;
                    state  <= S_ADDR_W;
                    shift_out <= {dev_addr, 1'b0}; // Addr + Write
                    bit_cnt   <= 7;
                end
            end

            S_ADDR_W: begin
                if (clk_tick && !clk_phase) begin
                    scl    <= 0;
                    sda_oe <= 1;
                    sda_o  <= shift_out[bit_cnt];
                end
                if (clk_tick && clk_phase) begin
                    scl <= 1;
                    if (bit_cnt == 0) begin
                        state <= S_ACK_AW;
                    end else begin
                        bit_cnt <= bit_cnt - 1;
                    end
                end
            end

            S_ACK_AW: begin
                if (clk_tick && !clk_phase) begin
                    scl    <= 0;
                    sda_oe <= 0; // Release for ACK
                end
                if (clk_tick && clk_phase) begin
                    scl   <= 1;
                    // Read ACK (ignore NACK for now)
                    state <= S_REG;
                    shift_out <= reg_addr;
                    bit_cnt   <= 7;
                end
            end

            S_REG: begin
                if (clk_tick && !clk_phase) begin
                    scl    <= 0;
                    sda_oe <= 1;
                    sda_o  <= shift_out[bit_cnt];
                end
                if (clk_tick && clk_phase) begin
                    scl <= 1;
                    if (bit_cnt == 0) begin
                        state <= S_ACK_REG;
                    end else begin
                        bit_cnt <= bit_cnt - 1;
                    end
                end
            end

            S_ACK_REG: begin
                if (clk_tick && !clk_phase) begin
                    scl    <= 0;
                    sda_oe <= 0;
                end
                if (clk_tick && clk_phase) begin
                    scl   <= 1;
                    state <= S_RESTART;
                end
            end

            S_RESTART: begin
                if (clk_tick && !clk_phase) begin
                    scl    <= 0;
                    sda_oe <= 0; // SDA high
                end
                if (clk_tick && clk_phase) begin
                    scl    <= 1;
                    sda_oe <= 1;
                    sda_o  <= 0; // SDA goes low = RESTART
                    state  <= S_ADDR_R;
                    shift_out <= {dev_addr, 1'b1}; // Addr + Read
                    bit_cnt   <= 7;
                end
            end

            S_ADDR_R: begin
                if (clk_tick && !clk_phase) begin
                    scl    <= 0;
                    sda_oe <= 1;
                    sda_o  <= shift_out[bit_cnt];
                end
                if (clk_tick && clk_phase) begin
                    scl <= 1;
                    if (bit_cnt == 0) begin
                        state <= S_ACK_AR;
                    end else begin
                        bit_cnt <= bit_cnt - 1;
                    end
                end
            end

            S_ACK_AR: begin
                if (clk_tick && !clk_phase) begin
                    scl    <= 0;
                    sda_oe <= 0;
                end
                if (clk_tick && clk_phase) begin
                    scl     <= 1;
                    state   <= S_READ;
                    bit_cnt <= 7;
                end
            end

            S_READ: begin
                if (clk_tick && !clk_phase) begin
                    scl    <= 0;
                    sda_oe <= 0; // Release for reading
                end
                if (clk_tick && clk_phase) begin
                    scl <= 1;
                    shift_in[bit_cnt] <= sda_i;
                    if (bit_cnt == 0) begin
                        state <= S_ACK_READ;
                    end else begin
                        bit_cnt <= bit_cnt - 1;
                    end
                end
            end

            S_ACK_READ: begin
                if (clk_tick && !clk_phase) begin
                    scl    <= 0;
                    sda_oe <= 1;
                    // Store received byte
                    data_out <= {data_out[39:0], shift_in};
                    byte_cnt <= byte_cnt + 1;
                    // ACK if more bytes to read, NACK if last byte
                    if (byte_cnt + 1 < bytes_to_read)
                        sda_o <= 0; // ACK
                    else
                        sda_o <= 1; // NACK (last byte)
                end
                if (clk_tick && clk_phase) begin
                    scl <= 1;
                    if (byte_cnt >= bytes_to_read) begin
                        state <= S_STOP;
                    end else begin
                        state   <= S_READ;
                        bit_cnt <= 7;
                    end
                end
            end

            S_STOP: begin
                if (clk_tick && !clk_phase) begin
                    scl    <= 0;
                    sda_oe <= 1;
                    sda_o  <= 0;
                end
                if (clk_tick && clk_phase) begin
                    scl        <= 1;
                    sda_oe     <= 0; // SDA goes high = STOP
                    data_valid <= 1;
                    busy       <= 0;
                    state      <= S_IDLE;
                end
            end
        endcase
    end
end

endmodule
