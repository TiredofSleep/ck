## ============================================================================
##  CK Master Constraint File — Puzhi PZ7020-StarLite (XC7Z020-2CLG400I)
##  Derived from official Puzhi examples via openeye-CamSI repository
##  Board: PZ7020-SL-C (SCFPGA / aithtech.com rebrand)
## ============================================================================

## ── Global Configuration ──
set_property CFGBVS VCCO [current_design]
set_property CONFIG_VOLTAGE 3.3 [current_design]
set_property BITSTREAM.GENERAL.COMPRESS true [current_design]
set_property BITSTREAM.CONFIG.CONFIGRATE 50 [current_design]
set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]
set_property BITSTREAM.CONFIG.SPI_FALL_EDGE Yes [current_design]

## ── System Clock (200 MHz differential, DDR3 reference) ──
set_property -dict {PACKAGE_PIN R4 IOSTANDARD DIFF_SSTL135} [get_ports sys_clk_p]
create_clock -period 5.000 -name sys_clk [get_ports sys_clk_p]

## ── System Reset (active low, directly accessible) ──
set_property -dict {PACKAGE_PIN R14 IOSTANDARD LVCMOS33} [get_ports sys_rst_n]

## ── On-Board LEDs (directly accessible, active high) ──
set_property -dict {PACKAGE_PIN W22 IOSTANDARD LVCMOS33} [get_ports {led[0]}]
set_property -dict {PACKAGE_PIN Y22 IOSTANDARD LVCMOS33} [get_ports {led[1]}]

## ── On-Board Keys/Buttons (directly accessible) ──
set_property -dict {PACKAGE_PIN W21 IOSTANDARD LVCMOS33} [get_ports {key[0]}]
set_property -dict {PACKAGE_PIN Y21 IOSTANDARD LVCMOS33} [get_ports {key[1]}]

## ── HDMI Output (on-board, active on PL) ──
set_property -dict {PACKAGE_PIN V17  IOSTANDARD TMDS_33} [get_ports hdmi_d2_p]
set_property -dict {PACKAGE_PIN AA19 IOSTANDARD TMDS_33} [get_ports hdmi_d1_p]
set_property -dict {PACKAGE_PIN V18  IOSTANDARD TMDS_33} [get_ports hdmi_d0_p]
set_property -dict {PACKAGE_PIN Y18  IOSTANDARD TMDS_33} [get_ports hdmi_clk_p]

## ── PL UART (directly accessible) ──
set_property -dict {PACKAGE_PIN P15 IOSTANDARD LVCMOS33} [get_ports uart_tx]
set_property -dict {PACKAGE_PIN P14 IOSTANDARD LVCMOS33} [get_ports uart_rx]

## ── E2PROM I2C (on-board) ──
set_property -dict {PACKAGE_PIN N13 IOSTANDARD LVCMOS33} [get_ports eeprom_scl]
set_property -dict {PACKAGE_PIN N14 IOSTANDARD LVCMOS33} [get_ports eeprom_sda]

## ── PL Gigabit Ethernet (RGMII, on-board) ──
set_property -dict {PACKAGE_PIN T20 IOSTANDARD LVCMOS33} [get_ports eth_rst_n]
set_property -dict {PACKAGE_PIN T18 IOSTANDARD LVCMOS33} [get_ports eth_mdc]
set_property -dict {PACKAGE_PIN N15 IOSTANDARD LVCMOS33} [get_ports eth_mdio]
set_property -dict {PACKAGE_PIN W19 IOSTANDARD LVCMOS33} [get_ports eth_rxc]
set_property -dict {PACKAGE_PIN W20 IOSTANDARD LVCMOS33} [get_ports eth_rx_ctl]
set_property -dict {PACKAGE_PIN U18 IOSTANDARD LVCMOS33} [get_ports {eth_rxd[0]}]
set_property -dict {PACKAGE_PIN R19 IOSTANDARD LVCMOS33} [get_ports {eth_rxd[1]}]
set_property -dict {PACKAGE_PIN R18 IOSTANDARD LVCMOS33} [get_ports {eth_rxd[2]}]
set_property -dict {PACKAGE_PIN P20 IOSTANDARD LVCMOS33} [get_ports {eth_rxd[3]}]
set_property -dict {PACKAGE_PIN P17 IOSTANDARD LVCMOS33} [get_ports eth_txc]
set_property -dict {PACKAGE_PIN R16 IOSTANDARD LVCMOS33} [get_ports eth_tx_ctl]
set_property -dict {PACKAGE_PIN P19 IOSTANDARD LVCMOS33} [get_ports {eth_txd[0]}]
set_property -dict {PACKAGE_PIN P16 IOSTANDARD LVCMOS33} [get_ports {eth_txd[1]}]
set_property -dict {PACKAGE_PIN N17 IOSTANDARD LVCMOS33} [get_ports {eth_txd[2]}]
set_property -dict {PACKAGE_PIN R17 IOSTANDARD LVCMOS33} [get_ports {eth_txd[3]}]
set_property SLEW FAST [get_ports eth_txc]
set_property SLEW FAST [get_ports eth_tx_ctl]
set_property SLEW FAST [get_ports {eth_txd[*]}]
create_clock -period 8.000 -name eth_rxc [get_ports eth_rxc]

## ============================================================================
##  40-Pin Expansion Port 1 (J1) — 32 user I/Os on PL Bank 13/35
##  Pin order: physical header pin → FPGA package pin
##  NOTE: Your LCD screen is plugged into this port
## ============================================================================

## ── J1 Expansion Port I/Os (active when LCD/AD_DA/Camera modules connected) ──
set_property -dict {PACKAGE_PIN F13 IOSTANDARD LVCMOS33} [get_ports {j1_io[0]}]
set_property -dict {PACKAGE_PIN E16 IOSTANDARD LVCMOS33} [get_ports {j1_io[1]}]
set_property -dict {PACKAGE_PIN F14 IOSTANDARD LVCMOS33} [get_ports {j1_io[2]}]
set_property -dict {PACKAGE_PIN D16 IOSTANDARD LVCMOS33} [get_ports {j1_io[3]}]
set_property -dict {PACKAGE_PIN D14 IOSTANDARD LVCMOS33} [get_ports {j1_io[4]}]
set_property -dict {PACKAGE_PIN C13 IOSTANDARD LVCMOS33} [get_ports {j1_io[5]}]
set_property -dict {PACKAGE_PIN D15 IOSTANDARD LVCMOS33} [get_ports {j1_io[6]}]
set_property -dict {PACKAGE_PIN B13 IOSTANDARD LVCMOS33} [get_ports {j1_io[7]}]
set_property -dict {PACKAGE_PIN C14 IOSTANDARD LVCMOS33} [get_ports {j1_io[8]}]
set_property -dict {PACKAGE_PIN A13 IOSTANDARD LVCMOS33} [get_ports {j1_io[9]}]
set_property -dict {PACKAGE_PIN C15 IOSTANDARD LVCMOS33} [get_ports {j1_io[10]}]
set_property -dict {PACKAGE_PIN A14 IOSTANDARD LVCMOS33} [get_ports {j1_io[11]}]
set_property -dict {PACKAGE_PIN E13 IOSTANDARD LVCMOS33} [get_ports {j1_io[12]}]
set_property -dict {PACKAGE_PIN A15 IOSTANDARD LVCMOS33} [get_ports {j1_io[13]}]
set_property -dict {PACKAGE_PIN E14 IOSTANDARD LVCMOS33} [get_ports {j1_io[14]}]
set_property -dict {PACKAGE_PIN A16 IOSTANDARD LVCMOS33} [get_ports {j1_io[15]}]
set_property -dict {PACKAGE_PIN B15 IOSTANDARD LVCMOS33} [get_ports {j1_io[16]}]
set_property -dict {PACKAGE_PIN B17 IOSTANDARD LVCMOS33} [get_ports {j1_io[17]}]
set_property -dict {PACKAGE_PIN B16 IOSTANDARD LVCMOS33} [get_ports {j1_io[18]}]
set_property -dict {PACKAGE_PIN B18 IOSTANDARD LVCMOS33} [get_ports {j1_io[19]}]
set_property -dict {PACKAGE_PIN F16 IOSTANDARD LVCMOS33} [get_ports {j1_io[20]}]
set_property -dict {PACKAGE_PIN D17 IOSTANDARD LVCMOS33} [get_ports {j1_io[21]}]
set_property -dict {PACKAGE_PIN E17 IOSTANDARD LVCMOS33} [get_ports {j1_io[22]}]
set_property -dict {PACKAGE_PIN C17 IOSTANDARD LVCMOS33} [get_ports {j1_io[23]}]
set_property -dict {PACKAGE_PIN F18 IOSTANDARD LVCMOS33} [get_ports {j1_io[24]}]
set_property -dict {PACKAGE_PIN C18 IOSTANDARD LVCMOS33} [get_ports {j1_io[25]}]
set_property -dict {PACKAGE_PIN E18 IOSTANDARD LVCMOS33} [get_ports {j1_io[26]}]
set_property -dict {PACKAGE_PIN C19 IOSTANDARD LVCMOS33} [get_ports {j1_io[27]}]
set_property -dict {PACKAGE_PIN A20 IOSTANDARD LVCMOS33} [get_ports {j1_io[28]}]
set_property -dict {PACKAGE_PIN E19 IOSTANDARD LVCMOS33} [get_ports {j1_io[29]}]
set_property -dict {PACKAGE_PIN B20 IOSTANDARD LVCMOS33} [get_ports {j1_io[30]}]
set_property -dict {PACKAGE_PIN D19 IOSTANDARD LVCMOS33} [get_ports {j1_io[31]}]

## ============================================================================
##  LCD Aliases (active when LCD screen connected to J1)
##  LCD uses 24-bit RGB parallel + clk/hs/vs = 27 pins
## ============================================================================
## lcd_rgb[0]  = j1_io[0]  = F13
## lcd_rgb[1]  = j1_io[1]  = E16
## lcd_rgb[2]  = j1_io[2]  = F14
## lcd_rgb[3]  = j1_io[3]  = D16
## lcd_rgb[4]  = j1_io[4]  = D14
## lcd_rgb[5]  = j1_io[5]  = C13
## lcd_rgb[6]  = j1_io[6]  = D15
## lcd_rgb[7]  = j1_io[7]  = B13
## lcd_rgb[8]  = j1_io[8]  = C14
## lcd_rgb[9]  = j1_io[9]  = A13
## lcd_rgb[10] = j1_io[10] = C15
## lcd_rgb[11] = j1_io[11] = A14
## lcd_rgb[12] = j1_io[12] = E13
## lcd_rgb[13] = j1_io[13] = A15
## lcd_rgb[14] = j1_io[14] = E14
## lcd_rgb[15] = j1_io[15] = A16
## lcd_rgb[16] = j1_io[16] = B15
## lcd_rgb[17] = j1_io[17] = B17
## lcd_rgb[18] = j1_io[18] = B16
## lcd_rgb[19] = j1_io[19] = B18
## lcd_rgb[20] = j1_io[20] = F16
## lcd_rgb[21] = j1_io[21] = D17
## lcd_rgb[22] = j1_io[22] = E17
## lcd_rgb[23] = j1_io[23] = C17
## lcd_clk     = j1_io[24] = F18
## lcd_hs      = j1_io[25] = C18
## lcd_vs      = j1_io[26] = E18

## ============================================================================
##  CK Heartbeat Signal Mapping (active port depends on what's connected)
##  When LCD is on J1, CK's non-display I/O goes through:
##    - j1_io[27..31] (5 spare pins on J1 beyond LCD's 27)
##    - On-board LEDs, keys, UART, Ethernet
##    - PS-side peripherals via AXI
## ============================================================================
