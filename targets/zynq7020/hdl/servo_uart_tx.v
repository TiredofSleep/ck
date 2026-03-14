/*
 * servo_uart_tx.v -- PL-Side UART Transmitter for Bus Servos
 * ===========================================================
 * Operator: BALANCE (5) -- precise bridge to the body.
 *
 * Simple UART TX for sending servo commands from PL fabric.
 * The PS UART is used for host (R16) communication.
 * This PL UART goes to the XiaoR servo bus.
 *
 * AXI-Lite mapped at CK_SERVO_UART_BASE (0x43C10000):
 *   +0x00 (W): TX data byte -- write starts transmission
 *   +0x04 (R): Status -- bit 0 = TX busy (FIFO full)
 *
 * 115200 baud, 8N1. Active on JM2 pin (configurable in XDC).
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

module servo_uart_tx #(
    parameter CLK_FREQ  = 100_000_000,
    parameter BAUD_RATE = 115200,
    parameter FIFO_DEPTH = 32
)(
    input  wire        clk,
    input  wire        rst_n,

    /* AXI-Lite register interface (directly mapped) */
    input  wire [7:0]  tx_data,        /* Byte to send */
    input  wire        tx_write,       /* Pulse to enqueue byte */
    output wire        tx_busy,        /* 1 = FIFO full or transmitting */

    /* Physical UART pin */
    output reg         uart_tx         /* Goes to JM2 pin -> servo bus */
);

    /* Baud rate divider: CLK_FREQ / BAUD_RATE */
    localparam BAUD_DIV = CLK_FREQ / BAUD_RATE;

    /* ── FIFO ── */
    reg [7:0]  fifo [0:FIFO_DEPTH-1];
    reg [5:0]  fifo_wr_ptr;
    reg [5:0]  fifo_rd_ptr;
    reg [5:0]  fifo_count;

    wire fifo_empty = (fifo_count == 0);
    wire fifo_full  = (fifo_count >= FIFO_DEPTH);
    assign tx_busy  = fifo_full;

    /* FIFO write */
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            fifo_wr_ptr <= 0;
        end else if (tx_write && !fifo_full) begin
            fifo[fifo_wr_ptr] <= tx_data;
            fifo_wr_ptr <= (fifo_wr_ptr == FIFO_DEPTH-1) ? 0 : fifo_wr_ptr + 1;
        end
    end

    /* ── TX State Machine ── */
    localparam S_IDLE  = 0;
    localparam S_START = 1;
    localparam S_DATA  = 2;
    localparam S_STOP  = 3;

    reg [1:0]  state;
    reg [15:0] baud_cnt;
    reg [2:0]  bit_idx;
    reg [7:0]  tx_shift;
    reg        fifo_pop;

    /* FIFO count management */
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            fifo_count <= 0;
        end else begin
            case ({(tx_write && !fifo_full), fifo_pop})
                2'b10: fifo_count <= fifo_count + 1;
                2'b01: fifo_count <= fifo_count - 1;
                default: fifo_count <= fifo_count;
            endcase
        end
    end

    /* TX state machine */
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state      <= S_IDLE;
            uart_tx    <= 1'b1;   /* Idle high */
            baud_cnt   <= 0;
            bit_idx    <= 0;
            tx_shift   <= 0;
            fifo_pop   <= 0;
            fifo_rd_ptr <= 0;
        end else begin
            fifo_pop <= 0;

            case (state)
                S_IDLE: begin
                    uart_tx <= 1'b1;
                    if (!fifo_empty) begin
                        /* Load byte from FIFO */
                        tx_shift <= fifo[fifo_rd_ptr];
                        fifo_rd_ptr <= (fifo_rd_ptr == FIFO_DEPTH-1) ? 0 : fifo_rd_ptr + 1;
                        fifo_pop <= 1;
                        baud_cnt <= 0;
                        state    <= S_START;
                    end
                end

                S_START: begin
                    uart_tx <= 1'b0;  /* Start bit */
                    if (baud_cnt >= BAUD_DIV - 1) begin
                        baud_cnt <= 0;
                        bit_idx  <= 0;
                        state    <= S_DATA;
                    end else begin
                        baud_cnt <= baud_cnt + 1;
                    end
                end

                S_DATA: begin
                    uart_tx <= tx_shift[bit_idx];  /* LSB first */
                    if (baud_cnt >= BAUD_DIV - 1) begin
                        baud_cnt <= 0;
                        if (bit_idx == 7) begin
                            state <= S_STOP;
                        end else begin
                            bit_idx <= bit_idx + 1;
                        end
                    end else begin
                        baud_cnt <= baud_cnt + 1;
                    end
                end

                S_STOP: begin
                    uart_tx <= 1'b1;  /* Stop bit */
                    if (baud_cnt >= BAUD_DIV - 1) begin
                        baud_cnt <= 0;
                        state    <= S_IDLE;
                    end else begin
                        baud_cnt <= baud_cnt + 1;
                    end
                end
            endcase
        end
    end

endmodule
