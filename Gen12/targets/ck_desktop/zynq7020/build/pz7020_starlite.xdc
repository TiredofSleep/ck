## ============================================================================
##  CK Standalone Board Constraints -- Puzhi PZ7020-StarLite
##  Only physical pins that CK actually uses. Nothing else.
##  T* = 5/7
## ============================================================================

## -- Global Configuration --
set_property CFGBVS VCCO [current_design]
set_property CONFIG_VOLTAGE 3.3 [current_design]
set_property BITSTREAM.GENERAL.COMPRESS true [current_design]

## -- System Clock (200 MHz differential) --
## Only constrain P pin; Vivado auto-maps N to the pair partner
set_property -dict {PACKAGE_PIN R4 IOSTANDARD DIFF_SSTL135} [get_ports sys_clk_p]
set_property -dict {PACKAGE_PIN T4 IOSTANDARD DIFF_SSTL135} [get_ports sys_clk_n]
create_clock -period 5.000 -name sys_clk [get_ports sys_clk_p]

## -- System Reset (active-low pushbutton) --
set_property -dict {PACKAGE_PIN R14 IOSTANDARD LVCMOS33} [get_ports sys_rst_n]

## -- On-Board LEDs (active high) --
set_property -dict {PACKAGE_PIN W22 IOSTANDARD LVCMOS33} [get_ports {led[0]}]
set_property -dict {PACKAGE_PIN Y22 IOSTANDARD LVCMOS33} [get_ports {led[1]}]

## -- On-Board Keys/Buttons (directly accessible) --
set_property -dict {PACKAGE_PIN W21 IOSTANDARD LVCMOS33} [get_ports {key[0]}]
set_property -dict {PACKAGE_PIN Y21 IOSTANDARD LVCMOS33} [get_ports {key[1]}]

## -- Timing: PLL output is the real system clock --
## All internal logic runs on the 100 MHz PLL output
## No false paths needed -- single clock domain
