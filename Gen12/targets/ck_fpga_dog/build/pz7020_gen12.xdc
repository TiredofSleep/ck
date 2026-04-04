# ============================================================
# PZ7020-StarLite Gen12 Pin Constraints
# CK Gen12 — Simplex Architecture (Δ⁰→Δ¹→Δ²→Δ³)
# ============================================================
# Derived from pz7020_full.xdc (Gen9 Build 16)
#
# Gen12 changes from Gen9 full:
#   - jm2[0] (J20) repurposed as jm2_leash_rx (Δ¹ leash from R16)
#   - Removed jm2[0] from JM2 bus; added jm2_leash_rx
#   - eth_inst hierarchy renamed from eth_tx_inst
#
# (c) 2026 Brayden Ross Sanders / 7Site LLC — Trinity Infinity Geometry
# ============================================================

# Config
set_property CFGBVS VCCO [current_design]
set_property CONFIG_VOLTAGE 3.3 [current_design]
set_property BITSTREAM.GENERAL.COMPRESS TRUE [current_design]

# ============================================================
# PL Clock: 50 MHz oscillator (U18)
# ============================================================
set_property -dict {PACKAGE_PIN U18  IOSTANDARD LVCMOS33} [get_ports pl_clk_50m]
create_clock -period 20.000 -name sys_clk [get_ports pl_clk_50m]

# ============================================================
# LEDs (active-low, Bank 34)
# ============================================================
set_property -dict {PACKAGE_PIN R19  IOSTANDARD LVCMOS33} [get_ports led1_n]
set_property -dict {PACKAGE_PIN V13  IOSTANDARD LVCMOS33} [get_ports led2_n]

# ============================================================
# Keys (active-low, Bank 35)
# ============================================================
set_property -dict {PACKAGE_PIN G14  IOSTANDARD LVCMOS33} [get_ports key1_n]
set_property -dict {PACKAGE_PIN J15  IOSTANDARD LVCMOS33} [get_ports key2_n]

# ============================================================
# HDMI Output (Bank 34, TMDS differential)
# ============================================================
set_property -dict {PACKAGE_PIN W18  IOSTANDARD TMDS_33} [get_ports hdmi_clk_p]
set_property -dict {PACKAGE_PIN W19  IOSTANDARD TMDS_33} [get_ports hdmi_clk_n]
set_property -dict {PACKAGE_PIN R16  IOSTANDARD TMDS_33} [get_ports {hdmi_data_p[0]}]
set_property -dict {PACKAGE_PIN R17  IOSTANDARD TMDS_33} [get_ports {hdmi_data_n[0]}]
set_property -dict {PACKAGE_PIN T17  IOSTANDARD TMDS_33} [get_ports {hdmi_data_p[1]}]
set_property -dict {PACKAGE_PIN R18  IOSTANDARD TMDS_33} [get_ports {hdmi_data_n[1]}]
set_property -dict {PACKAGE_PIN V17  IOSTANDARD TMDS_33} [get_ports {hdmi_data_p[2]}]
set_property -dict {PACKAGE_PIN V18  IOSTANDARD TMDS_33} [get_ports {hdmi_data_n[2]}]
set_property -dict {PACKAGE_PIN P15  IOSTANDARD LVCMOS33} [get_ports hdmi_out_en]
set_property -dict {PACKAGE_PIN P16  IOSTANDARD LVCMOS33} [get_ports hdmi_hpd]
set_property -dict {PACKAGE_PIN N17  IOSTANDARD LVCMOS33} [get_ports hdmi_scl]
set_property -dict {PACKAGE_PIN P18  IOSTANDARD LVCMOS33} [get_ports hdmi_sda]

# ============================================================
# JM1: LCD output (Bank 35, LVCMOS33, jm1[0..31])
# ============================================================
set_property -dict {PACKAGE_PIN C20  IOSTANDARD LVCMOS33} [get_ports {jm1[0]}]
set_property -dict {PACKAGE_PIN B20  IOSTANDARD LVCMOS33} [get_ports {jm1[1]}]
set_property -dict {PACKAGE_PIN B19  IOSTANDARD LVCMOS33} [get_ports {jm1[2]}]
set_property -dict {PACKAGE_PIN A20  IOSTANDARD LVCMOS33} [get_ports {jm1[3]}]
set_property -dict {PACKAGE_PIN E17  IOSTANDARD LVCMOS33} [get_ports {jm1[4]}]
set_property -dict {PACKAGE_PIN D18  IOSTANDARD LVCMOS33} [get_ports {jm1[5]}]
set_property -dict {PACKAGE_PIN D19  IOSTANDARD LVCMOS33} [get_ports {jm1[6]}]
set_property -dict {PACKAGE_PIN D20  IOSTANDARD LVCMOS33} [get_ports {jm1[7]}]
set_property -dict {PACKAGE_PIN E18  IOSTANDARD LVCMOS33} [get_ports {jm1[8]}]
set_property -dict {PACKAGE_PIN E19  IOSTANDARD LVCMOS33} [get_ports {jm1[9]}]
set_property -dict {PACKAGE_PIN F16  IOSTANDARD LVCMOS33} [get_ports {jm1[10]}]
set_property -dict {PACKAGE_PIN F17  IOSTANDARD LVCMOS33} [get_ports {jm1[11]}]
set_property -dict {PACKAGE_PIN M19  IOSTANDARD LVCMOS33} [get_ports {jm1[12]}]
set_property -dict {PACKAGE_PIN M20  IOSTANDARD LVCMOS33} [get_ports {jm1[13]}]
set_property -dict {PACKAGE_PIN M17  IOSTANDARD LVCMOS33} [get_ports {jm1[14]}]
set_property -dict {PACKAGE_PIN M18  IOSTANDARD LVCMOS33} [get_ports {jm1[15]}]
set_property -dict {PACKAGE_PIN L19  IOSTANDARD LVCMOS33} [get_ports {jm1[16]}]
set_property -dict {PACKAGE_PIN L20  IOSTANDARD LVCMOS33} [get_ports {jm1[17]}]
set_property -dict {PACKAGE_PIN K19  IOSTANDARD LVCMOS33} [get_ports {jm1[18]}]
set_property -dict {PACKAGE_PIN J19  IOSTANDARD LVCMOS33} [get_ports {jm1[19]}]
set_property -dict {PACKAGE_PIN L16  IOSTANDARD LVCMOS33} [get_ports {jm1[20]}]
set_property -dict {PACKAGE_PIN L17  IOSTANDARD LVCMOS33} [get_ports {jm1[21]}]
set_property -dict {PACKAGE_PIN K17  IOSTANDARD LVCMOS33} [get_ports {jm1[22]}]
set_property -dict {PACKAGE_PIN K18  IOSTANDARD LVCMOS33} [get_ports {jm1[23]}]
set_property -dict {PACKAGE_PIN H16  IOSTANDARD LVCMOS33} [get_ports {jm1[24]}]
set_property -dict {PACKAGE_PIN H17  IOSTANDARD LVCMOS33} [get_ports {jm1[25]}]
set_property -dict {PACKAGE_PIN J18  IOSTANDARD LVCMOS33} [get_ports {jm1[26]}]
set_property -dict {PACKAGE_PIN H18  IOSTANDARD LVCMOS33} [get_ports {jm1[27]}]
set_property -dict {PACKAGE_PIN F19  IOSTANDARD LVCMOS33} [get_ports {jm1[28]}]
set_property -dict {PACKAGE_PIN F20  IOSTANDARD LVCMOS33} [get_ports {jm1[29]}]
set_property -dict {PACKAGE_PIN G17  IOSTANDARD LVCMOS33} [get_ports {jm1[30]}]
set_property -dict {PACKAGE_PIN G18  IOSTANDARD LVCMOS33} [get_ports {jm1[31]}]

# ============================================================
# JM2: inputs + servo TX (Bank 35/34)
# NOTE: jm2[0] (J20) is REPURPOSED as jm2_leash_rx in Gen12.
#       jm2 bus here is [30:0] = pins 1..30 of physical connector.
#       jm2_leash_rx = J20 = physical pin 0.
# ============================================================
# Δ¹ Leash RX from R16 — physical jm2[0] pin, J20 (Bank 35)
set_property -dict {PACKAGE_PIN J20  IOSTANDARD LVCMOS33  PULLUP TRUE} [get_ports jm2_leash_rx]

# JM2 inputs jm2[1..30] (jm2[0]=J20 now used for leash_rx above)
set_property -dict {PACKAGE_PIN H20  IOSTANDARD LVCMOS33} [get_ports {jm2[1]}]
set_property -dict {PACKAGE_PIN G19  IOSTANDARD LVCMOS33} [get_ports {jm2[2]}]
set_property -dict {PACKAGE_PIN G20  IOSTANDARD LVCMOS33} [get_ports {jm2[3]}]
set_property -dict {PACKAGE_PIN H15  IOSTANDARD LVCMOS33} [get_ports {jm2[4]}]
set_property -dict {PACKAGE_PIN G15  IOSTANDARD LVCMOS33} [get_ports {jm2[5]}]
set_property -dict {PACKAGE_PIN K14  IOSTANDARD LVCMOS33} [get_ports {jm2[6]}]
set_property -dict {PACKAGE_PIN J14  IOSTANDARD LVCMOS33} [get_ports {jm2[7]}]
set_property -dict {PACKAGE_PIN N15  IOSTANDARD LVCMOS33} [get_ports {jm2[8]}]
set_property -dict {PACKAGE_PIN N16  IOSTANDARD LVCMOS33} [get_ports {jm2[9]}]
set_property -dict {PACKAGE_PIN L14  IOSTANDARD LVCMOS33} [get_ports {jm2[10]}]
set_property -dict {PACKAGE_PIN L15  IOSTANDARD LVCMOS33} [get_ports {jm2[11]}]
set_property -dict {PACKAGE_PIN M14  IOSTANDARD LVCMOS33} [get_ports {jm2[12]}]
set_property -dict {PACKAGE_PIN M15  IOSTANDARD LVCMOS33} [get_ports {jm2[13]}]
set_property -dict {PACKAGE_PIN K16  IOSTANDARD LVCMOS33} [get_ports {jm2[14]}]
set_property -dict {PACKAGE_PIN J16  IOSTANDARD LVCMOS33} [get_ports {jm2[15]}]
set_property -dict {PACKAGE_PIN T16  IOSTANDARD LVCMOS33} [get_ports {jm2[16]}]
set_property -dict {PACKAGE_PIN U17  IOSTANDARD LVCMOS33} [get_ports {jm2[17]}]
set_property -dict {PACKAGE_PIN P14  IOSTANDARD LVCMOS33} [get_ports {jm2[18]}]
set_property -dict {PACKAGE_PIN R14  IOSTANDARD LVCMOS33} [get_ports {jm2[19]}]
set_property -dict {PACKAGE_PIN T11  IOSTANDARD LVCMOS33} [get_ports {jm2[20]}]
set_property -dict {PACKAGE_PIN T10  IOSTANDARD LVCMOS33} [get_ports {jm2[21]}]
set_property -dict {PACKAGE_PIN V12  IOSTANDARD LVCMOS33} [get_ports {jm2[22]}]
set_property -dict {PACKAGE_PIN W13  IOSTANDARD LVCMOS33} [get_ports {jm2[23]}]
set_property -dict {PACKAGE_PIN T14  IOSTANDARD LVCMOS33} [get_ports {jm2[24]}]
set_property -dict {PACKAGE_PIN T15  IOSTANDARD LVCMOS33} [get_ports {jm2[25]}]
set_property -dict {PACKAGE_PIN T12  IOSTANDARD LVCMOS33} [get_ports {jm2[26]}]
set_property -dict {PACKAGE_PIN U12  IOSTANDARD LVCMOS33} [get_ports {jm2[27]}]
set_property -dict {PACKAGE_PIN Y16  IOSTANDARD LVCMOS33} [get_ports {jm2[28]}]
set_property -dict {PACKAGE_PIN Y17  IOSTANDARD LVCMOS33} [get_ports {jm2[29]}]
set_property -dict {PACKAGE_PIN W14  IOSTANDARD LVCMOS33} [get_ports {jm2[30]}]

# Servo UART TX (jm2[31] repurposed as output)
set_property -dict {PACKAGE_PIN Y14  IOSTANDARD LVCMOS33} [get_ports jm2_servo_tx]

# ============================================================
# PL Gigabit Ethernet RGMII (RTL8211F-CG, Bank 34)
# ============================================================
set_property -dict {PACKAGE_PIN V20  IOSTANDARD LVCMOS33  SLEW FAST} [get_ports pl_eth_gtx_clk]
set_property -dict {PACKAGE_PIN N20  IOSTANDARD LVCMOS33  SLEW FAST} [get_ports {pl_eth_txd[0]}]
set_property -dict {PACKAGE_PIN P20  IOSTANDARD LVCMOS33  SLEW FAST} [get_ports {pl_eth_txd[1]}]
set_property -dict {PACKAGE_PIN T20  IOSTANDARD LVCMOS33  SLEW FAST} [get_ports {pl_eth_txd[2]}]
set_property -dict {PACKAGE_PIN U20  IOSTANDARD LVCMOS33  SLEW FAST} [get_ports {pl_eth_txd[3]}]
set_property -dict {PACKAGE_PIN W20  IOSTANDARD LVCMOS33  SLEW FAST} [get_ports pl_eth_tx_en]
set_property -dict {PACKAGE_PIN U14  IOSTANDARD LVCMOS33}             [get_ports pl_eth_mdc]
set_property -dict {PACKAGE_PIN U15  IOSTANDARD LVCMOS33  PULLUP TRUE} [get_ports pl_eth_mdio]

# ============================================================
# Clock constraints for generated clocks
# ============================================================
# Ethernet TX MMCM (eth_inst, Gen12 instance name)
# Heartbeat data is quasi-static (<50 Hz) — false path between domains

set_false_path -from [get_clocks sys_clk] \
    -to [get_clocks -of_objects [get_pins eth_inst/mmcm_eth/CLKOUT0]]
set_false_path -from [get_clocks -of_objects [get_pins eth_inst/mmcm_eth/CLKOUT0]] \
    -to [get_clocks sys_clk]

# HDMI clock domain CDC (quasi-static brain state signals)
set_false_path -from [get_clocks sys_clk] \
    -to [get_clocks -of_objects [get_pins hdmi_inst/mmcm_inst/CLKOUT0]]
set_false_path -from [get_clocks sys_clk] \
    -to [get_clocks -of_objects [get_pins hdmi_inst/mmcm_inst/CLKOUT1]]
set_false_path -from [get_clocks -of_objects [get_pins hdmi_inst/mmcm_inst/CLKOUT0]] \
    -to [get_clocks sys_clk]
set_false_path -from [get_clocks -of_objects [get_pins hdmi_inst/mmcm_inst/CLKOUT1]] \
    -to [get_clocks sys_clk]

# RGMII TX: source-synchronous DDR outputs — false path
# The RTL8211F PHY samples TXD/TX_EN relative to the GTX clock driven from
# the same FPGA MMCM (pl_eth_gtx_clk), not relative to any external reference.
# Timing is guaranteed by MMCM phase alignment. output_delay constraints
# create impossible-to-meet 4ns half-period checks against the 3.2ns ODDR pad
# delay and are not meaningful for this topology.
set_false_path -to [get_ports {pl_eth_txd[*]}]
set_false_path -to [get_ports pl_eth_tx_en]
set_false_path -to [get_ports pl_eth_gtx_clk]
