# ============================================================
# program_gen12.tcl — Program Gen12 Bitstream via JTAG
# ============================================================
# Programs ck_gen12.bit into the PZ7020-StarLite via JTAG.
# Run from Vivado Tcl Console or batch mode.
#
# Requirements:
#   - JTAG cable connected (USB, Digilent JTAG-HS2 or similar)
#   - JTAG jumper set on board (J1 or per board manual)
#   - ck_gen12.bit present in same directory as this script
#     (run build_gen12.tcl first if not already built)
#
# Usage:
#   vivado -mode batch -source program_gen12.tcl
#   (or paste into Vivado Tcl Console)
#
# (c) 2026 Brayden Ross Sanders / 7Site LLC — Trinity Infinity Geometry
# ============================================================

set script_dir [file dirname [file normalize [info script]]]
set bit_file   [file normalize "$script_dir/ck_gen12.bit"]

if {![file exists $bit_file]} {
    puts ""
    puts "  [ERROR] Bitstream not found: $bit_file"
    puts "  Run build_gen12.tcl first."
    puts ""
    return 1
}

puts ""
puts "  ========================================================"
puts "  CK Gen12 — JTAG Programming"
puts "  ========================================================"
puts "  Bitstream: $bit_file"
puts "  Size:      [file size $bit_file] bytes"
puts ""

open_hw_manager
connect_hw_server -allow_non_jtag

if {[catch {open_hw_target} err]} {
    puts ""
    puts "  [ERROR] Could not open JTAG target: $err"
    puts "  Check USB cable and JTAG jumper position."
    puts ""
    close_hw_manager
    return 1
}

# Get XC7Z020 device
set dev ""
foreach d [get_hw_devices] {
    if {[string match "*xc7z020*" $d] || [string match "*xc7z0*" $d]} {
        set dev $d
        break
    }
}

if {$dev eq ""} {
    puts "  [WARN] xc7z020 not found by name — using first device"
    set all_devs [get_hw_devices]
    if {[llength $all_devs] == 0} {
        puts "  [ERROR] No JTAG devices found."
        close_hw_target
        disconnect_hw_server
        close_hw_manager
        return 1
    }
    set dev [lindex $all_devs 0]
}

puts "  Device:   $dev"
puts "  Programming..."
puts ""

current_hw_device $dev
set_property PROGRAM.FILE $bit_file $dev
program_hw_devices $dev

puts ""
puts "  ========================================================"
puts "  Gen12 programmed."
puts "  ========================================================"
puts ""
puts "  Expected behavior:"
puts "    LED1 (R19) blinking at ~50 Hz  — Δ⁰ heartbeat alive"
puts "    LED2 (V13) solid               — Δ³ T* reached (TROT)"
puts "    LED2 (V13) dim/off             — Δ⁰/Δ¹/Δ² below threshold"
puts ""
puts "  Next step — Δ¹ leash test:"
puts "    cd Gen12\\targets\\ck_fpga_dog"
puts "    python ck_leash_test.py COM3 --verbose --no-servo"
puts ""
puts "  T* = 5/7 is in silicon."
puts ""

close_hw_target
disconnect_hw_server
close_hw_manager
