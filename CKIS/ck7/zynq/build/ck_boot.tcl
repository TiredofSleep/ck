#
# ck_boot.tcl -- Vivado Block Design for CK Coherence Machine
# ==============================================================
# Operator: LATTICE (1) -- structure that holds everything.
#
# Creates the Zynq PS + CK Heartbeat IP block design.
# Run in Vivado Tcl console:
#   source /path/to/ck_boot.tcl
#
# Prerequisites:
#   1. Create Vivado project targeting xc7z020clg400-1 (Zynq-7020)
#   2. Add ck_heartbeat.v as a design source
#   3. Package ck_heartbeat as AXI-Lite IP (or use GPIO bridge)
#   4. Source this script to wire up the block design
#
# (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
#

# ── Project Settings ──
# Adjust these for your specific Puzhi board
set PART "xc7z020clg400-1"
set BOARD_FREQ_MHZ 50
set CPU_FREQ_MHZ 667

# ── Create Block Design ──
create_bd_design "ck_system"

# ── Add Zynq PS ──
set ps [create_bd_cell -type ip -vlnv xilinx.com:ip:processing_system7:5.5 ps7]

# Configure PS
set_property -dict [list \
    CONFIG.PCW_FPGA0_PERIPHERAL_FREQMHZ {100} \
    CONFIG.PCW_USE_M_AXI_GP0 {1} \
    CONFIG.PCW_USE_FABRIC_INTERRUPT {0} \
    CONFIG.PCW_UART0_PERIPHERAL_ENABLE {1} \
    CONFIG.PCW_UART0_UART0_IO {MIO 14 .. 15} \
    CONFIG.PCW_UART1_PERIPHERAL_ENABLE {1} \
    CONFIG.PCW_UART1_UART1_IO {MIO 48 .. 49} \
    CONFIG.PCW_SD0_PERIPHERAL_ENABLE {1} \
    CONFIG.PCW_GPIO_EMIO_GPIO_ENABLE {1} \
    CONFIG.PCW_GPIO_EMIO_GPIO_IO {4} \
] $ps

# Apply board preset if available
# apply_bd_automation -rule xilinx.com:bd_rule:processing_system7

# ── Add AXI GPIO for LEDs ──
set gpio_led [create_bd_cell -type ip -vlnv xilinx.com:ip:axi_gpio:2.0 axi_gpio_led]
set_property -dict [list \
    CONFIG.C_GPIO_WIDTH {4} \
    CONFIG.C_ALL_OUTPUTS {1} \
] $gpio_led

# ── Add AXI GPIO for Heartbeat Interface ──
# Channel 1: Write registers (phase_b, phase_d, tick_strobe, enable) = 16 bits
# Channel 2: Read registers (phase_bc, tick_count, coh_num, coh_den, etc.)
# NOTE: For production, package ck_heartbeat.v as proper AXI-Lite IP.
#       This GPIO approach works for Phase 0 bring-up.
set gpio_hb_wr [create_bd_cell -type ip -vlnv xilinx.com:ip:axi_gpio:2.0 axi_gpio_hb_wr]
set_property -dict [list \
    CONFIG.C_GPIO_WIDTH {32} \
    CONFIG.C_ALL_OUTPUTS {1} \
    CONFIG.C_IS_DUAL {0} \
] $gpio_hb_wr

set gpio_hb_rd [create_bd_cell -type ip -vlnv xilinx.com:ip:axi_gpio:2.0 axi_gpio_hb_rd]
set_property -dict [list \
    CONFIG.C_GPIO_WIDTH {32} \
    CONFIG.C_ALL_INPUTS {1} \
    CONFIG.C_IS_DUAL {1} \
    CONFIG.C_IS_DUAL {1} \
    CONFIG.C_GPIO2_WIDTH {32} \
    CONFIG.C_ALL_INPUTS_2 {1} \
] $gpio_hb_rd

# ── Add AXI Interconnect ──
set axi_ic [create_bd_cell -type ip -vlnv xilinx.com:ip:axi_interconnect:2.1 axi_interconnect_0]
set_property CONFIG.NUM_MI {3} $axi_ic

# ── Add Processor System Reset ──
set rst [create_bd_cell -type ip -vlnv xilinx.com:ip:proc_sys_reset:5.0 proc_sys_reset_0]

# ── Connect Clocks and Resets ──
connect_bd_net [get_bd_pins ps7/FCLK_CLK0] \
    [get_bd_pins axi_interconnect_0/ACLK] \
    [get_bd_pins axi_interconnect_0/S00_ACLK] \
    [get_bd_pins axi_interconnect_0/M00_ACLK] \
    [get_bd_pins axi_interconnect_0/M01_ACLK] \
    [get_bd_pins axi_interconnect_0/M02_ACLK] \
    [get_bd_pins axi_gpio_led/s_axi_aclk] \
    [get_bd_pins axi_gpio_hb_wr/s_axi_aclk] \
    [get_bd_pins axi_gpio_hb_rd/s_axi_aclk] \
    [get_bd_pins proc_sys_reset_0/slowest_sync_clk]

connect_bd_net [get_bd_pins ps7/FCLK_RESET0_N] \
    [get_bd_pins proc_sys_reset_0/ext_reset_in]

connect_bd_net [get_bd_pins proc_sys_reset_0/peripheral_aresetn] \
    [get_bd_pins axi_interconnect_0/ARESETN] \
    [get_bd_pins axi_interconnect_0/S00_ARESETN] \
    [get_bd_pins axi_interconnect_0/M00_ARESETN] \
    [get_bd_pins axi_interconnect_0/M01_ARESETN] \
    [get_bd_pins axi_interconnect_0/M02_ARESETN] \
    [get_bd_pins axi_gpio_led/s_axi_aresetn] \
    [get_bd_pins axi_gpio_hb_wr/s_axi_aresetn] \
    [get_bd_pins axi_gpio_hb_rd/s_axi_aresetn]

# ── Connect AXI Master ──
connect_bd_intf_net [get_bd_intf_pins ps7/M_AXI_GP0] \
    [get_bd_intf_pins axi_interconnect_0/S00_AXI]

connect_bd_intf_net [get_bd_intf_pins axi_interconnect_0/M00_AXI] \
    [get_bd_intf_pins axi_gpio_led/S_AXI]

connect_bd_intf_net [get_bd_intf_pins axi_interconnect_0/M01_AXI] \
    [get_bd_intf_pins axi_gpio_hb_wr/S_AXI]

connect_bd_intf_net [get_bd_intf_pins axi_interconnect_0/M02_AXI] \
    [get_bd_intf_pins axi_gpio_hb_rd/S_AXI]

# ── Address Map ──
# LED GPIO:        0x41200000 (matches CK_LED_GPIO_BASE in ck_led.h)
# Heartbeat Write: 0x41210000
# Heartbeat Read:  0x41220000
assign_bd_address
set_property offset 0x41200000 [get_bd_addr_segs {ps7/Data/SEG_axi_gpio_led_Reg}]
set_property offset 0x41210000 [get_bd_addr_segs {ps7/Data/SEG_axi_gpio_hb_wr_Reg}]
set_property offset 0x41220000 [get_bd_addr_segs {ps7/Data/SEG_axi_gpio_hb_rd_Reg}]

# ── DDR and Fixed IO (required for PS) ──
apply_bd_automation -rule xilinx.com:bd_rule:processing_system7 \
    -config {make_external "FIXED_IO, DDR"} $ps

# ── Validate and Save ──
validate_bd_design
save_bd_design

# ── Generate HDL Wrapper ──
make_wrapper -files [get_files ck_system.bd] -top
add_files -norecurse [get_files -filter {FILE_TYPE == "VHDL" || FILE_TYPE == "Verilog"} ck_system_wrapper*]

puts ""
puts "╔══════════════════════════════════════════════════╗"
puts "║  CK Coherence Machine -- Block Design Complete   ║"
puts "║                                                  ║"
puts "║  Next steps:                                     ║"
puts "║  1. Add ck_heartbeat.v to sources                ║"
puts "║  2. Wire heartbeat ports to GPIO pins            ║"
puts "║  3. Run Synthesis + Implementation               ║"
puts "║  4. Generate Bitstream                           ║"
puts "║  5. Export Hardware (.xsa) for Vitis              ║"
puts "║  6. Create Vitis bare metal app with ck_main.c   ║"
puts "║  7. Build BOOT.BIN → microSD → power on          ║"
puts "╚══════════════════════════════════════════════════╝"
puts ""
