# ck_zynq7020.tcl -- Vivado Build Script for CK Zynq-7020 Dog Platform
# =====================================================================
# Creates a complete Vivado project with Zynq PS + CK PL modules.
#
# Usage: In Vivado Tcl console:
#   cd <path-to-zynq7020/build>
#   source ck_zynq7020.tcl
#
# Target: Zybo Z7-20 (xc7z020clg400-1)
#
# (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory

set project_name "ck_zynq7020"
set part_name "xc7z020clg400-1"
set hdl_dir "../hdl"
set fpga_hdl_dir "../../fpga/hdl"

# ── Create project ──
create_project $project_name ./$project_name -part $part_name -force

# ── Add HDL sources ──
# New Zynq-7020 modules
add_files -norecurse [glob $hdl_dir/*.v]

# Reused FPGA modules (heartbeat, D2, DAC, I2S)
add_files -norecurse $fpga_hdl_dir/ck_heartbeat.v
add_files -norecurse $fpga_hdl_dir/d2_pipeline.v
add_files -norecurse $fpga_hdl_dir/dac_spi.v
add_files -norecurse $fpga_hdl_dir/i2s_receiver.v

# ── Set top module ──
set_property top ck_top_zynq7020 [current_fileset]

# ── Create block design with Zynq PS ──
create_bd_design "ck_system"

# Add Zynq PS
create_bd_cell -type ip -vlnv xilinx.com:ip:processing_system7:5.5 processing_system7_0

# Configure Zynq PS
set_property -dict [list \
    CONFIG.PCW_FPGA0_PERIPHERAL_FREQMHZ {100} \
    CONFIG.PCW_USE_M_AXI_GP0 {1} \
    CONFIG.PCW_UART0_PERIPHERAL_ENABLE {1} \
    CONFIG.PCW_UART0_UART0_IO {MIO 14 .. 15} \
    CONFIG.PCW_GPIO_MIO_GPIO_ENABLE {1} \
] [get_bd_cells processing_system7_0]

# Apply board preset if available (Zybo Z7)
# apply_board_connection -board_interface "ddr" -ip_intf "processing_system7_0/DDR"
# apply_board_connection -board_interface "fixed_io" -ip_intf "processing_system7_0/FIXED_IO"

# ── Connect clocks and resets ──
# FCLK_CLK0 = 100 MHz -> PL clock
# FCLK_RESET0_N -> PL reset

puts "============================================="
puts " CK Zynq-7020 Project Created Successfully"
puts " Part: $part_name"
puts " HDL files added from: $hdl_dir, $fpga_hdl_dir"
puts ""
puts " Next steps:"
puts "   1. Run synthesis: launch_runs synth_1"
puts "   2. Run implementation: launch_runs impl_1"
puts "   3. Generate bitstream: write_bitstream"
puts "   4. Export hardware: write_hw_platform"
puts "============================================="
