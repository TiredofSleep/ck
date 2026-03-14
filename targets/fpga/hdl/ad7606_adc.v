/*
 * ad7606_adc.v -- Parallel ADC Interface for AD7606 (PZ-AD7606 Module)
 * ====================================================================
 * Operator: RECEPTION (2) -- CK receives the world through his ears.
 *
 * Drives the AD7606 8-channel 16-bit simultaneous-sampling ADC
 * on the PZ7606 ADDA module plugged into JM2.
 *
 * AD7606 conversion cycle:
 *   1. CONVST rising edge -> samples all 8 channels simultaneously
 *   2. BUSY goes HIGH during conversion (~4 us)
 *   3. BUSY falls -> data ready
 *   4. Assert CS low, pulse RD low for each channel read (8 reads)
 *   5. DB[15:0] presents signed 16-bit data on each RD pulse
 *
 * For CK's ears: Channel 0 = left mic, Channel 1 = right mic.
 * Other channels available for additional sensors.
 *
 * Sample rate controlled by CONVST period. At 48 kHz:
 *   Period = 100 MHz / 48000 = 2083 clocks (~20.83 us)
 *   Conversion takes ~4 us, read takes ~1 us, plenty of margin.
 *
 * AXI interface:
 *   Offset 0x00: CH0 data [15:0] (read-only, signed)
 *   Offset 0x04: CH1 data [15:0]
 *   Offset 0x08: CH2 data [15:0]
 *   Offset 0x0C: CH3 data [15:0]
 *   Offset 0x10: CH4 data [15:0]
 *   Offset 0x14: CH5 data [15:0]
 *   Offset 0x18: CH6 data [15:0]
 *   Offset 0x1C: CH7 data [15:0]
 *   Offset 0x20: Status [1:0] = {data_valid, busy}
 *   Offset 0x24: FIFO CH0 read (for audio streaming)
 *   Offset 0x28: FIFO status [8:0] = fifo_count
 *   Offset 0x2C: Sample rate divider (write)
 *
 * FIFO: Channel 0 samples are pushed into a 512-deep FIFO for
 * audio streaming. ARM reads from FIFO at its own pace.
 *
 * Target: Zynq-7020 Artix-7 fabric, 100 MHz system clock.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

module ad7606_adc #(
    parameter CLK_FREQ     = 100_000_000,
    parameter SAMPLE_RATE  = 48_000,       // Default 48 kHz
    parameter FIFO_DEPTH   = 512,          // Audio FIFO depth
    parameter NUM_CHANNELS = 8
)(
    input  wire        clk,
    input  wire        rst_n,

    // AXI-side interface (ARM reads samples here)
    input  wire [3:0]  reg_addr,          // Register address (word-aligned >> 2)
    input  wire        reg_rd,            // Read strobe
    input  wire        reg_wr,            // Write strobe
    input  wire [31:0] reg_wdata,         // Write data
    output reg  [31:0] reg_rdata,         // Read data

    // AD7606 parallel interface (directly to PZ7606 module via JM2)
    input  wire [15:0] adc_db,            // Parallel data bus DB[15:0]
    input  wire        adc_busy,          // BUSY output from AD7606
    output reg         adc_convst,        // CONVST (start conversion)
    output reg         adc_rd_n,          // RD (read strobe, active low)
    output reg         adc_cs_n,          // CS (chip select, active low)
    output reg         adc_reset,         // RESET (active high)
    output wire [2:0]  adc_os             // Oversampling: 000 = none
);

    // -- No oversampling for audio rate --
    assign adc_os = 3'b000;

    // -- Sample Rate Divider --
    reg [31:0] rate_div;
    wire [31:0] rate_div_val = CLK_FREQ / SAMPLE_RATE;
    reg [31:0] rate_cnt;

    // -- Channel Data Registers --
    reg [15:0] ch_data [0:NUM_CHANNELS-1];
    reg        data_valid;

    // -- Audio FIFO (Channel 0 only, for mic streaming) --
    reg [15:0] fifo_mem [0:FIFO_DEPTH-1];
    reg [$clog2(FIFO_DEPTH)-1:0] fifo_wr_ptr;
    reg [$clog2(FIFO_DEPTH)-1:0] fifo_rd_ptr;
    reg [$clog2(FIFO_DEPTH):0]   fifo_level;
    wire fifo_full  = (fifo_level >= FIFO_DEPTH);
    wire fifo_empty = (fifo_level == 0);

    // -- State Machine --
    localparam S_RESET    = 3'd0;
    localparam S_IDLE     = 3'd1;
    localparam S_CONVST   = 3'd2;
    localparam S_WAIT     = 3'd3;
    localparam S_READ     = 3'd4;
    localparam S_RD_PULSE = 3'd5;
    localparam S_CAPTURE  = 3'd6;
    localparam S_DONE     = 3'd7;

    reg [2:0] state;
    reg [3:0] ch_idx;           // Channel being read (0-7)
    reg [7:0] wait_cnt;         // Wait counter for timing
    reg [15:0] reset_cnt;       // Reset pulse counter

    // -- Reset sequence (100 us pulse on power-up) --
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state      <= S_RESET;
            adc_convst <= 0;
            adc_rd_n   <= 1;
            adc_cs_n   <= 1;
            adc_reset  <= 1;  // Assert reset
            ch_idx     <= 0;
            wait_cnt   <= 0;
            reset_cnt  <= 0;
            data_valid <= 0;
            rate_div   <= rate_div_val;
            rate_cnt   <= 0;
            fifo_wr_ptr <= 0;
            fifo_rd_ptr <= 0;
            fifo_level  <= 0;
        end else begin
            case (state)
                S_RESET: begin
                    // Hold reset for 10000 clocks (~100 us)
                    if (reset_cnt >= 10000) begin
                        adc_reset <= 0;
                        state <= S_IDLE;
                    end else begin
                        reset_cnt <= reset_cnt + 1;
                    end
                end

                S_IDLE: begin
                    adc_convst <= 0;
                    adc_rd_n   <= 1;
                    adc_cs_n   <= 1;
                    // Count down to next conversion
                    if (rate_cnt >= rate_div) begin
                        rate_cnt <= 0;
                        state    <= S_CONVST;
                    end else begin
                        rate_cnt <= rate_cnt + 1;
                    end
                end

                S_CONVST: begin
                    // Rising edge of CONVST starts simultaneous sampling
                    adc_convst <= 1;
                    wait_cnt   <= 0;
                    state      <= S_WAIT;
                end

                S_WAIT: begin
                    // Hold CONVST high briefly, then wait for BUSY to fall
                    adc_convst <= 0;
                    if (!adc_busy && wait_cnt > 10) begin
                        // Conversion done, start reading
                        ch_idx   <= 0;
                        adc_cs_n <= 0;  // Assert chip select
                        state    <= S_READ;
                    end else begin
                        wait_cnt <= wait_cnt + 1;
                        // Safety timeout: if BUSY never asserts after 500 clocks,
                        // proceed anyway (handles disconnected ADC gracefully)
                        if (wait_cnt >= 200) begin
                            ch_idx   <= 0;
                            adc_cs_n <= 0;
                            state    <= S_READ;
                        end
                    end
                end

                S_READ: begin
                    // Assert RD low to gate data onto DB bus
                    adc_rd_n <= 0;
                    wait_cnt <= 0;
                    state    <= S_RD_PULSE;
                end

                S_RD_PULSE: begin
                    // Wait 3 clocks for data to settle (30 ns at 100 MHz)
                    if (wait_cnt >= 3) begin
                        state <= S_CAPTURE;
                    end else begin
                        wait_cnt <= wait_cnt + 1;
                    end
                end

                S_CAPTURE: begin
                    // Latch data from DB bus
                    ch_data[ch_idx] <= adc_db;
                    adc_rd_n <= 1;  // Deassert RD

                    // Push channel 0 into audio FIFO
                    if (ch_idx == 0 && !fifo_full) begin
                        fifo_mem[fifo_wr_ptr] <= adc_db;
                        fifo_wr_ptr <= fifo_wr_ptr + 1;
                        fifo_level  <= fifo_level + 1;
                    end

                    if (ch_idx >= NUM_CHANNELS - 1) begin
                        state <= S_DONE;
                    end else begin
                        ch_idx <= ch_idx + 1;
                        state  <= S_READ;
                    end
                end

                S_DONE: begin
                    adc_cs_n   <= 1;
                    data_valid <= 1;
                    state      <= S_IDLE;
                end
            endcase

            // FIFO read (when ARM reads from FIFO register)
            if (reg_rd && reg_addr == 4'd9) begin  // 0x24 >> 2 = 9
                if (!fifo_empty) begin
                    fifo_rd_ptr <= fifo_rd_ptr + 1;
                    fifo_level  <= fifo_level - 1;
                end
            end

            // Sample rate update
            if (reg_wr && reg_addr == 4'd11) begin  // 0x2C >> 2 = 11
                rate_div <= reg_wdata;
            end
        end
    end

    // -- Register Read Mux --
    always @(*) begin
        case (reg_addr)
            4'd0:  reg_rdata = {16'd0, ch_data[0]};   // 0x00: CH0
            4'd1:  reg_rdata = {16'd0, ch_data[1]};   // 0x04: CH1
            4'd2:  reg_rdata = {16'd0, ch_data[2]};   // 0x08: CH2
            4'd3:  reg_rdata = {16'd0, ch_data[3]};   // 0x0C: CH3
            4'd4:  reg_rdata = {16'd0, ch_data[4]};   // 0x10: CH4
            4'd5:  reg_rdata = {16'd0, ch_data[5]};   // 0x14: CH5
            4'd6:  reg_rdata = {16'd0, ch_data[6]};   // 0x18: CH6
            4'd7:  reg_rdata = {16'd0, ch_data[7]};   // 0x1C: CH7
            4'd8:  reg_rdata = {30'd0, data_valid, adc_busy};  // 0x20: Status
            4'd9:  reg_rdata = {16'd0, fifo_mem[fifo_rd_ptr]}; // 0x24: FIFO read
            4'd10: reg_rdata = {23'd0, fifo_level};    // 0x28: FIFO count
            4'd11: reg_rdata = rate_div;                // 0x2C: Rate divider
            default: reg_rdata = 32'd0;
        endcase
    end

endmodule
