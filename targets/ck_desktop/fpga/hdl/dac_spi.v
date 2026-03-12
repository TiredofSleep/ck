/*
 * dac_spi.v -- SPI Master for DAC128S085 (8-channel, 12-bit DAC)
 * ================================================================
 * Operator: PROGRESS (3) -- CK's voice pushes outward.
 *
 * Drives the DAC128S085 on the PZ7606 ADDA module.
 * Takes a 12-bit sample + 3-bit channel select from the ARM
 * (via AXI register), clocks it out over SPI.
 *
 * DAC128S085 SPI protocol:
 *   16-bit word: [X][ADDR:3][DATA:12]
 *   MSB first, CPOL=0, CPHA=0 (SPI Mode 0)
 *   SCLK max: 40 MHz
 *   CS (SYNC) active low
 *   Data latched on rising SCLK edge
 *
 * For audio: ARM writes samples at 44.1kHz or 48kHz rate.
 * The FIFO decouples ARM timing from SPI clocking.
 *
 * Target: Zynq-7020 Artix-7 fabric, 100 MHz system clock.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

module dac_spi #(
    parameter CLK_FREQ   = 100_000_000,  // System clock (100 MHz)
    parameter SPI_FREQ   = 20_000_000,   // SPI clock (20 MHz, conservative)
    parameter FIFO_DEPTH = 256           // Sample FIFO depth
)(
    input  wire        clk,
    input  wire        rst_n,

    // AXI-side interface (ARM writes samples here)
    input  wire [15:0] sample_in,      // [15] unused, [14:12] channel, [11:0] data
    input  wire        sample_valid,   // Pulse to push into FIFO
    output wire        fifo_full,
    output wire        fifo_empty,
    output wire [7:0]  fifo_count,     // How many samples in FIFO

    // SPI pins (directly to DAC128S085 on PZ7606)
    output reg         spi_sclk,
    output reg         spi_mosi,
    output reg         spi_cs_n        // SYNC pin, active low
);

    // -- SPI Clock Divider --
    localparam CLK_DIV = CLK_FREQ / SPI_FREQ / 2;  // Half-period in clocks
    reg [$clog2(CLK_DIV)-1:0] clk_cnt;
    reg spi_clk_en;  // Pulses at 2x SPI_FREQ

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            clk_cnt <= 0;
            spi_clk_en <= 0;
        end else begin
            if (clk_cnt >= CLK_DIV - 1) begin
                clk_cnt <= 0;
                spi_clk_en <= 1;
            end else begin
                clk_cnt <= clk_cnt + 1;
                spi_clk_en <= 0;
            end
        end
    end

    // -- FIFO (simple ring buffer) --
    reg [15:0] fifo_mem [0:FIFO_DEPTH-1];
    reg [$clog2(FIFO_DEPTH)-1:0] fifo_wr_ptr;
    reg [$clog2(FIFO_DEPTH)-1:0] fifo_rd_ptr;
    reg [$clog2(FIFO_DEPTH):0]   fifo_level;

    assign fifo_full  = (fifo_level >= FIFO_DEPTH);
    assign fifo_empty = (fifo_level == 0);
    assign fifo_count = fifo_level[$clog2(FIFO_DEPTH):0];

    // FIFO write (from ARM)
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            fifo_wr_ptr <= 0;
        end else if (sample_valid && !fifo_full) begin
            fifo_mem[fifo_wr_ptr] <= sample_in;
            fifo_wr_ptr <= fifo_wr_ptr + 1;
        end
    end

    // -- SPI Transmit State Machine --
    localparam S_IDLE     = 2'd0;
    localparam S_LOAD     = 2'd1;
    localparam S_TRANSMIT = 2'd2;
    localparam S_DONE     = 2'd3;

    reg [1:0] state;
    reg [15:0] shift_reg;
    reg [4:0]  bit_cnt;      // 0-15 for 16-bit word
    reg        spi_phase;    // 0=setup, 1=sample (toggle with spi_clk_en)

    // FIFO read + SPI transmit
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state     <= S_IDLE;
            spi_sclk  <= 0;
            spi_mosi  <= 0;
            spi_cs_n  <= 1;  // Deasserted
            shift_reg <= 0;
            bit_cnt   <= 0;
            spi_phase <= 0;
            fifo_rd_ptr <= 0;
            fifo_level  <= 0;
        end else begin
            // FIFO level tracking
            case ({sample_valid && !fifo_full, state == S_LOAD && !fifo_empty})
                2'b10: fifo_level <= fifo_level + 1;
                2'b01: fifo_level <= fifo_level - 1;
                default: ; // No change or simultaneous read/write
            endcase

            if (spi_clk_en) begin
                case (state)
                    S_IDLE: begin
                        spi_sclk <= 0;
                        spi_cs_n <= 1;
                        if (!fifo_empty) begin
                            state <= S_LOAD;
                        end
                    end

                    S_LOAD: begin
                        // Load next sample from FIFO
                        shift_reg <= fifo_mem[fifo_rd_ptr];
                        fifo_rd_ptr <= fifo_rd_ptr + 1;
                        bit_cnt   <= 15;  // Start from MSB
                        spi_cs_n  <= 0;   // Assert CS
                        spi_phase <= 0;
                        state     <= S_TRANSMIT;
                    end

                    S_TRANSMIT: begin
                        if (spi_phase == 0) begin
                            // Setup phase: put data on MOSI, SCLK low
                            spi_sclk <= 0;
                            spi_mosi <= shift_reg[bit_cnt];
                            spi_phase <= 1;
                        end else begin
                            // Sample phase: SCLK high (DAC latches on rising edge)
                            spi_sclk <= 1;
                            spi_phase <= 0;
                            if (bit_cnt == 0) begin
                                state <= S_DONE;
                            end else begin
                                bit_cnt <= bit_cnt - 1;
                            end
                        end
                    end

                    S_DONE: begin
                        spi_sclk <= 0;
                        spi_cs_n <= 1;  // Deassert CS (DAC updates output)
                        state    <= S_IDLE;
                    end
                endcase
            end
        end
    end

endmodule
